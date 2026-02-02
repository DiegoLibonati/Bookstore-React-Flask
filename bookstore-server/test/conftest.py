import os
import subprocess
import time
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from pymongo import MongoClient
from pymongo.database import Database

from app import create_app
from config.mongo_config import mongo

TEST_MONGO_HOST = os.getenv("TEST_MONGO_HOST", "localhost")
TEST_MONGO_PORT = int(os.getenv("TEST_MONGO_PORT", "27018"))
TEST_MONGO_USER = os.getenv("TEST_MONGO_USER", "admin")
TEST_MONGO_PASS = os.getenv("TEST_MONGO_PASS", "secret123")
TEST_MONGO_DB = os.getenv("TEST_MONGO_DB", "test_db")
TEST_MONGO_URI = f"mongodb://{TEST_MONGO_USER}:{TEST_MONGO_PASS}@{TEST_MONGO_HOST}:{TEST_MONGO_PORT}/{TEST_MONGO_DB}?authSource=admin"


def is_mongo_ready(uri: str, timeout: int = 30) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=1000)
            client.admin.command("ping")
            client.close()
            return True
        except Exception:
            time.sleep(1)
    return False


def start_docker_compose() -> None:
    compose_file = os.path.join(
        os.path.dirname(__file__), "..", "test.docker-compose.yml"
    )

    if not os.path.exists(compose_file):
        raise FileNotFoundError(
            f"The docker-compose file was not found: {compose_file}"
        )

    subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "-d", "--wait"],
        check=True,
        capture_output=True,
    )


def stop_docker_compose() -> None:
    compose_file = os.path.join(
        os.path.dirname(__file__), "..", "test.docker-compose.yml"
    )

    subprocess.run(
        ["docker", "compose", "-f", compose_file, "down", "-v"],
        check=False,
        capture_output=True,
    )


def clean_all_collections(db: Database) -> None:
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})


@pytest.fixture(scope="session")
def docker_compose_up() -> Generator[None, None, None]:
    skip_docker = os.getenv("SKIP_DOCKER_COMPOSE", "").lower() in ("true", "1", "yes")

    if not skip_docker:
        print("\n🐳 Starting test containers...")
        try:
            start_docker_compose()
        except subprocess.CalledProcessError as e:
            print(f"Error starting docker-compose: {e}")
            raise

    if not is_mongo_ready(TEST_MONGO_URI):
        raise RuntimeError("MongoDB is unavailable after the timeout.")

    print("✅ MongoDB ready for testing.")

    yield

    if not skip_docker:
        print("\n🧹 Stopping test containers...")
        stop_docker_compose()


@pytest.fixture(scope="session")
def mongo_client(
    docker_compose_up: Generator[None, None, None]
) -> Generator[MongoClient, None, None]:
    client = MongoClient(TEST_MONGO_URI)
    yield client
    client.close()


@pytest.fixture(scope="session")
def mongo_db(mongo_client: MongoClient) -> Database:
    return mongo_client[TEST_MONGO_DB]


@pytest.fixture(scope="function")
def clean_db(mongo_db: Database) -> Generator[Database, None, None]:
    clean_all_collections(mongo_db)

    yield mongo_db

    clean_all_collections(mongo_db)


@pytest.fixture(scope="function")
def app(mongo_db: Database) -> Generator[Flask, None, None]:
    os.environ["MONGO_URI"] = TEST_MONGO_URI
    os.environ["MONGO_DB_NAME"] = TEST_MONGO_DB
    os.environ["MONGO_HOST"] = TEST_MONGO_HOST
    os.environ["MONGO_PORT"] = str(TEST_MONGO_PORT)

    clean_all_collections(mongo_db)

    application = create_app("testing")
    application.config["TESTING"] = True

    mongo.client = MongoClient(TEST_MONGO_URI)
    mongo.db = mongo.client[TEST_MONGO_DB]

    with application.app_context():
        yield application

    clean_all_collections(mongo_db)

    if mongo.client:
        mongo.client.close()


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


# ============================================================================
# Test data fixtures
# ============================================================================


@pytest.fixture
def sample_book() -> dict[str, str]:
    return {
        "image": "test_image.jpg",
        "title": "Drácula Test",
        "author": "Bram Stoker Test",
        "description": "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897. Test.",
        "genre": "Test",
    }


@pytest.fixture
def sample_books() -> list[dict[str, str]]:
    return [
        {
            "image": "test_image_2.jpg",
            "title": "Frankenstein Test",
            "author": "Mary Shelley Test",
            "description": "Es una novela de ciencia ficción gótica escrita por Mary Shelley, publicada en 1818. Test.",
            "genre": "Test",
        },
        {
            "image": "test_image_3.jpg",
            "title": "El extraño caso del Dr. Jekyll y Mr. Hyde Test",
            "author": "Robert Louis Stevenson Test",
            "description": "Es una novela corta de terror gótico escrita por Robert Louis Stevenson, publicada en 1886. Test.",
            "genre": "Test",
        },
        {
            "image": "test_image_4.jpg",
            "title": "El retrato de Dorian Gray Test",
            "author": "Oscar Wilde Test",
            "description": "Es una novela filosófica gótica escrita por Oscar Wilde, publicada en 1890. Test.",
            "genre": "Test",
        },
    ]


@pytest.fixture
def inserted_books(
    mongo_db: Database,
    sample_books: list[dict[str, str]],
) -> list[dict[str, str]]:
    inserted = []
    for book in sample_books:
        result = mongo_db.books.insert_one(book.copy())
        inserted.append(
            {
                **book,
                "_id": str(result.inserted_id),
            }
        )
    return inserted

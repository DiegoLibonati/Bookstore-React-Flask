import subprocess
import time

import pytest

from flask import Flask
from flask import Response
from flask.testing import FlaskClient

from src.app import app as api_app
from src.app import init


prefix_books_bp = "/api/v1/bookstore/books"
prefix_genres_bp = "/api/v1/bookstore/genres"


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = api_app
    init()
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def mongo_test_db():
    start = subprocess.run(
        ["docker-compose", "up", "-d", "bookstore-db"],
        capture_output=True,
        text=True,
    )

    time.sleep(5)

    yield

    down = subprocess.run(
        ["docker-compose", "down"],
        capture_output=True,
        text=True,
    )


@pytest.fixture(scope="session")
def dracula_book() -> dict[str, str]:
    dracula_book = {
        "image": "https://es.wikipedia.org/wiki/Archivo:Dracula-First-Edition-1897.jpg",
        "title": "Drácula",
        "author": "Bram Stoker",
        "description": "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897.",
        "genre": "Terror"
    }

    return dracula_book


@pytest.fixture(scope="session")
def inserted_book_id(flask_client: Flask, dracula_book: dict[str, str]) -> str:
    """Fixture to insert a book and return its ID."""
    response: Response = flask_client.post(
        f"{prefix_books_bp}/add",
        json=dracula_book,
    )
    result = response.json
    book = result.get("data")
    return book.get("_id")

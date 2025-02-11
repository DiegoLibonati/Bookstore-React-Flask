import subprocess
import time

import pytest

from flask import Flask
from flask.testing import FlaskClient

from src.app import app as api_app
from src.app import init
from src.data_access.books_repository import BookRepository
from src.models.Book import Book
from src.models.BookManager import BookManager

from test.constants import BOOK_MOCK


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = api_app
    init()
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def mongo_test_db() -> None:
    subprocess.run(
        ["docker-compose", "up", "-d", "bookstore-db"],
        capture_output=True,
        text=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "down"],
        capture_output=True,
        text=True,
    )


@pytest.fixture(scope="session")
def dracula_book() -> dict[str, str]:
    dracula_book = {
        "image": "test_image.jpg",
        "title": "Drácula Test",
        "author": "Bram Stoker Test",
        "description": "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897. Test.",
        "genre": "Test"
    }

    return dracula_book


@pytest.fixture(scope="session")
def book_test(dracula_book: dict[str, str]) -> dict[str, str]:
    _id = BOOK_MOCK["not_found_flag_id"]
    return {"_id": _id, **dracula_book}


@pytest.fixture(scope="session")
def book_repository(flask_app: Flask) -> BookRepository:
    return BookRepository(db=flask_app.mongo.db)


@pytest.fixture(scope="session")
def book_model(book_test: dict[str, str]) -> Book:
    return Book(**book_test)


@pytest.fixture(scope="session")
def book_manager_model() -> BookManager:
    return BookManager()
import subprocess
import time
from test.constants import BOOK_MOCK

import pytest
from bson import ObjectId
from flask import Blueprint, Flask, Response, jsonify
from flask.testing import FlaskClient
from pydantic import BaseModel
from pymongo.errors import PyMongoError

from app import create_app
from src.models.book_model import BookModel
from src.utils.error_handler import handle_exceptions
from src.utils.exceptions import ValidationAPIError


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = create_app()
    return app


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture
def error_app() -> FlaskClient:
    app = Flask(__name__)
    bp = Blueprint("test_errors", __name__)

    @bp.route("/base-api-error")
    @handle_exceptions
    def raise_base_api_error() -> None:
        raise ValidationAPIError(message="Custom API error")

    @bp.route("/pydantic-error")
    @handle_exceptions
    def raise_pydantic_error() -> Response:
        class Model(BaseModel):
            x: int

        Model(x="not-an-int")
        return jsonify({"ok": True})

    @bp.route("/mongo-error")
    @handle_exceptions
    def raise_mongo_error() -> None:
        raise PyMongoError("Mongo failed")

    @bp.route("/generic-error")
    @handle_exceptions
    def raise_generic_error() -> None:
        raise RuntimeError("Unexpected failure")

    @bp.route("/no-error")
    @handle_exceptions
    def no_error() -> Response:
        return jsonify({"ok": True})

    app.register_blueprint(bp)
    return app.test_client()


@pytest.fixture(scope="session")
def mongo_test_db() -> None:
    subprocess.run(
        ["docker-compose", "-f", "dev.docker-compose.yml", "up", "-d", "bookstore-db"],
        check=True,
        capture_output=True,
        text=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "-f", "dev.docker-compose.yml", "down"],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture(scope="session")
def dracula_book() -> dict[str, str]:
    return {
        "image": "test_image.jpg",
        "title": "Drácula Test",
        "author": "Bram Stoker Test",
        "description": "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897. Test.",
        "genre": "Test",
    }


@pytest.fixture(scope="session")
def book_test(dracula_book: dict[str, str]) -> dict[str, str]:
    _id = ObjectId(BOOK_MOCK["not_found_book_id"])
    return {"_id": _id, **dracula_book}


@pytest.fixture
def book_model(dracula_book: dict[str, str]) -> BookModel:
    return BookModel(
        image=dracula_book.get("image"),
        title=dracula_book.get("title"),
        author=dracula_book.get("author"),
        description=dracula_book.get("description"),
        genre=dracula_book.get("genre"),
    )

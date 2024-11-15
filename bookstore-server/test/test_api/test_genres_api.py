import pytest

from flask import Flask
from flask import Response

from test.conftest import prefix_genres_bp


def test_alive_genres(flask_client: Flask) -> None:
    response: Response = flask_client.get(f"{prefix_genres_bp}/alive")
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    version_bp = result.get("version_bp")
    author = result.get("author")
    name_bp = result.get("name_bp")

    assert status_code == 200
    assert message == "I am Alive!"
    assert version_bp == "2.0.0"
    assert author == "Diego Libonati"
    assert name_bp == "Genres"


def test_get_all_genres(flask_client: Flask, dracula_book: dict[str, str]) -> None:
    response: Response = flask_client.get(f"{prefix_genres_bp}/")
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    genres = result.get("data")

    assert status_code == 200
    assert message == "The book genres were successfully obtained."
    assert type(genres) == list
    assert dracula_book.get("genre") in genres
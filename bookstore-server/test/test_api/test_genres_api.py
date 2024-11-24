from flask import Flask
from flask import Response

from test.constants import BLUEPRINTS


def test_alive_genres(flask_client: Flask) -> None:
    response: Response = flask_client.get(f"{BLUEPRINTS['genres']}/alive")

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


def test_get_all_genres(flask_client: Flask) -> None:
    response: Response = flask_client.get(f"{BLUEPRINTS['genres']}/")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == "The book genres were successfully obtained."
    assert type(data) == list


    if data: assert data
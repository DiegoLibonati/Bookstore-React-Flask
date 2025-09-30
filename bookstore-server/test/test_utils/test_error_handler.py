from flask.testing import FlaskClient

from src.constants.codes import (
    CODE_ERROR_DATABASE,
    CODE_ERROR_GENERIC,
    CODE_ERROR_PYDANTIC,
)
from src.constants.messages import (
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_PYDANTIC,
)
from src.utils.exceptions import ValidationAPIError


def test_base_api_error(error_app: FlaskClient) -> None:
    response = error_app.get("/base-api-error")
    assert response.status_code == 400
    data = response.get_json()
    assert data["code"] == ValidationAPIError().code
    assert data["message"] == "Custom API error"


def test_pydantic_error(error_app: FlaskClient) -> None:
    response = error_app.get("/pydantic-error")
    assert response.status_code == 400
    data = response.get_json()
    assert data["code"] == CODE_ERROR_PYDANTIC
    assert data["message"] == MESSAGE_ERROR_PYDANTIC
    assert "details" in data["payload"]


def test_mongo_error(error_app: FlaskClient) -> None:
    response = error_app.get("/mongo-error")
    assert response.status_code == 500
    data = response.get_json()
    assert data["code"] == CODE_ERROR_DATABASE
    assert data["message"] == MESSAGE_ERROR_DATABASE


def test_generic_error(error_app: FlaskClient) -> None:
    response = error_app.get("/generic-error")
    assert response.status_code == 500
    data = response.get_json()
    assert data["code"] == CODE_ERROR_GENERIC
    assert data["message"].startswith(MESSAGE_ERROR_GENERIC.split("{")[0])


def test_no_error(error_app: FlaskClient) -> None:
    response = error_app.get("/no-error")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"ok": True}

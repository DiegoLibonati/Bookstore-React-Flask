from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.constants.codes import CODE_SUCCESS_HEALTH, CODE_SUCCESS_READY
from src.constants.messages import MESSAGE_SUCCESS_HEALTH, MESSAGE_SUCCESS_READY
from src.controllers.health_controller import health, ready


@pytest.fixture()
def standalone_app() -> Flask:
    app: Flask = Flask(__name__)
    app.add_url_rule("/health", view_func=health, methods=["GET"])
    app.add_url_rule("/ready", view_func=ready, methods=["GET"])
    return app


@pytest.fixture()
def standalone_client(standalone_app: Flask) -> FlaskClient:
    return standalone_app.test_client()


@pytest.mark.unit
class TestHealthController:
    def test_returns_200_status(self, standalone_client: FlaskClient) -> None:
        response = standalone_client.get("/health")

        assert response.status_code == 200

    def test_returns_success_health_code(self, standalone_client: FlaskClient) -> None:
        response = standalone_client.get("/health")
        data: dict[str, Any] = response.get_json()

        assert data["code"] == CODE_SUCCESS_HEALTH

    def test_returns_success_health_message(self, standalone_client: FlaskClient) -> None:
        response = standalone_client.get("/health")
        data: dict[str, Any] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_HEALTH


@pytest.mark.unit
class TestReadyController:
    def test_returns_200_status(self, standalone_client: FlaskClient) -> None:
        response = standalone_client.get("/ready")

        assert response.status_code == 200

    def test_returns_success_ready_code(self, standalone_client: FlaskClient) -> None:
        response = standalone_client.get("/ready")
        data: dict[str, Any] = response.get_json()

        assert data["code"] == CODE_SUCCESS_READY

    def test_returns_success_ready_message(self, standalone_client: FlaskClient) -> None:
        response = standalone_client.get("/ready")
        data: dict[str, Any] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_READY


@pytest.mark.integration
class TestHealthEndpointThroughApp:
    def test_returns_200_status(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")

        assert response.status_code == 200

    def test_returns_success_health_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, Any] = response.get_json()

        assert data["code"] == CODE_SUCCESS_HEALTH

    def test_returns_success_health_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, Any] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_HEALTH

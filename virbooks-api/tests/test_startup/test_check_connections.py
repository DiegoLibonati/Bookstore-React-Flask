import logging
from unittest.mock import MagicMock, call, patch

import pytest
from flask import Flask
from pymongo.errors import ServerSelectionTimeoutError

from app import create_app
from src.startup.check_connections import (
    CONNECT_TIMEOUT_MS,
    MAX_ATTEMPTS,
    RETRY_DELAY_SECONDS,
    check_connections,
    check_mongo_connection,
)

LOGGER_NAME = "src.startup.check_connections"


def make_app(mongo_uri: str | None = "mongodb://localhost:27017") -> Flask:
    app: Flask = Flask(__name__)
    if mongo_uri is not None:
        app.config["MONGO_URI"] = mongo_uri
    return app


@pytest.mark.unit
class TestCheckMongoConnection:
    def test_success_on_first_attempt_does_not_retry_or_warn(self, caplog: pytest.LogCaptureFixture) -> None:
        app: Flask = make_app()

        with (
            patch("src.startup.check_connections.MongoClient") as mock_mongo_client,
            patch("src.startup.check_connections.sleep") as mock_sleep,
            caplog.at_level(logging.DEBUG, logger=LOGGER_NAME),
        ):
            result: bool = check_mongo_connection(app)

        assert result is True
        mock_mongo_client.assert_called_once()
        mock_sleep.assert_not_called()
        warnings: list[logging.LogRecord] = [r for r in caplog.records if r.levelno == logging.WARNING]
        infos: list[logging.LogRecord] = [r for r in caplog.records if r.levelno == logging.INFO]
        assert len(warnings) == 0
        assert len(infos) == 1
        assert "attempt 1/5" in infos[0].getMessage()

    def test_success_on_third_attempt_warns_twice_and_stops_retrying(self, caplog: pytest.LogCaptureFixture) -> None:
        app: Flask = make_app()

        with (
            patch("src.startup.check_connections.MongoClient") as mock_mongo_client,
            patch("src.startup.check_connections.sleep") as mock_sleep,
            caplog.at_level(logging.DEBUG, logger=LOGGER_NAME),
        ):
            mock_client: MagicMock = MagicMock()
            mock_client.admin.command.side_effect = [
                ServerSelectionTimeoutError("down"),
                ServerSelectionTimeoutError("down"),
                {"ok": 1},
            ]
            mock_mongo_client.return_value = mock_client
            result: bool = check_mongo_connection(app)

        assert result is True
        assert mock_mongo_client.call_count == 3
        assert mock_sleep.call_args_list == [call(RETRY_DELAY_SECONDS), call(RETRY_DELAY_SECONDS)]
        warnings: list[logging.LogRecord] = [r for r in caplog.records if r.levelno == logging.WARNING]
        infos: list[logging.LogRecord] = [r for r in caplog.records if r.levelno == logging.INFO]
        assert len(warnings) == 2
        assert len(infos) == 1
        assert "attempt 3/5" in infos[0].getMessage()

    def test_five_failures_emit_final_warning_and_return_normally(self, caplog: pytest.LogCaptureFixture) -> None:
        app: Flask = make_app()

        with (
            patch("src.startup.check_connections.MongoClient") as mock_mongo_client,
            patch("src.startup.check_connections.sleep") as mock_sleep,
            caplog.at_level(logging.DEBUG, logger=LOGGER_NAME),
        ):
            mock_client: MagicMock = MagicMock()
            mock_client.admin.command.side_effect = ServerSelectionTimeoutError("down")
            mock_mongo_client.return_value = mock_client
            result: bool = check_mongo_connection(app)

        assert result is False
        assert mock_mongo_client.call_count == MAX_ATTEMPTS
        assert mock_sleep.call_count == MAX_ATTEMPTS - 1
        warnings: list[logging.LogRecord] = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == MAX_ATTEMPTS + 1
        assert "The app will continue running" in warnings[-1].getMessage()

    def test_missing_mongo_uri_skips_connection_attempt(self, caplog: pytest.LogCaptureFixture) -> None:
        app: Flask = make_app(mongo_uri=None)

        with (
            patch("src.startup.check_connections.MongoClient") as mock_mongo_client,
            caplog.at_level(logging.DEBUG, logger=LOGGER_NAME),
        ):
            result: bool = check_mongo_connection(app)

        assert result is False
        mock_mongo_client.assert_not_called()

    def test_client_uses_short_timeout_and_is_closed(self) -> None:
        app: Flask = make_app()

        with patch("src.startup.check_connections.MongoClient") as mock_mongo_client:
            mock_client: MagicMock = MagicMock()
            mock_mongo_client.return_value = mock_client
            check_mongo_connection(app)

        _, kwargs = mock_mongo_client.call_args
        assert kwargs["serverSelectionTimeoutMS"] == CONNECT_TIMEOUT_MS
        mock_client.close.assert_called_once()


@pytest.mark.unit
class TestCheckConnections:
    def test_runs_every_registered_check(self) -> None:
        app: Flask = make_app()
        first_check: MagicMock = MagicMock(return_value=True)
        second_check: MagicMock = MagicMock(return_value=True)

        with patch(
            "src.startup.check_connections.CONNECTION_CHECKS",
            [("First", first_check), ("Second", second_check)],
        ):
            check_connections(app)

        first_check.assert_called_once_with(app)
        second_check.assert_called_once_with(app)

    def test_one_failing_service_does_not_prevent_next_check(self, caplog: pytest.LogCaptureFixture) -> None:
        app: Flask = make_app()
        first_check: MagicMock = MagicMock(side_effect=RuntimeError("boom"))
        second_check: MagicMock = MagicMock(return_value=True)

        with (
            patch(
                "src.startup.check_connections.CONNECTION_CHECKS",
                [("First", first_check), ("Second", second_check)],
            ),
            caplog.at_level(logging.DEBUG, logger=LOGGER_NAME),
        ):
            check_connections(app)

        first_check.assert_called_once_with(app)
        second_check.assert_called_once_with(app)


@pytest.mark.unit
class TestCheckConnectionsWiring:
    def test_create_app_skips_checks_when_check_connections_is_false(self) -> None:
        with patch("app.check_connections") as mock_check_connections:
            create_app("testing")

        mock_check_connections.assert_not_called()

    def test_create_app_runs_checks_when_check_connections_is_true(self) -> None:
        with patch("app.check_connections") as mock_check_connections:
            app: Flask = create_app("development")

        mock_check_connections.assert_called_once_with(app)

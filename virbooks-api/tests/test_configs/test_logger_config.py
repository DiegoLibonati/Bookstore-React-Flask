import logging

import pytest

from src.configs.logger_config import setup_logger


@pytest.mark.unit
class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test_returns_logger_instance")
        assert isinstance(logger, logging.Logger)

    def test_logger_has_correct_name(self) -> None:
        logger: logging.Logger = setup_logger("test_logger_has_correct_name")
        assert logger.name == "test_logger_has_correct_name"

    def test_logger_has_at_least_one_handler(self) -> None:
        logger: logging.Logger = setup_logger("test_logger_has_at_least_one_handler")
        assert len(logger.handlers) >= 1

    def test_calling_twice_does_not_duplicate_handlers(self) -> None:
        logger: logging.Logger = setup_logger("test_calling_twice_does_not_duplicate_handlers")
        initial_count: int = len(logger.handlers)
        setup_logger("test_calling_twice_does_not_duplicate_handlers")
        assert len(logger.handlers) == initial_count

    def test_default_name_is_flask_app(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "flask-app"

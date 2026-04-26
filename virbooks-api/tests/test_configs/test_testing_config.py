import pytest

from src.configs.default_config import DefaultConfig
from src.configs.testing_config import TestingConfig


@pytest.mark.unit
class TestTestingConfig:
    def test_testing_is_true(self) -> None:
        assert TestingConfig.TESTING is True

    def test_debug_is_true(self) -> None:
        assert TestingConfig.DEBUG is True

    def test_env_is_testing(self) -> None:
        assert TestingConfig.ENV == "testing"

    def test_inherits_from_default_config(self) -> None:
        assert issubclass(TestingConfig, DefaultConfig)

    def test_mongo_uri_is_set_from_env(self) -> None:
        assert isinstance(TestingConfig.MONGO_URI, str)
        assert TestingConfig.MONGO_URI.startswith("mongodb://")

    def test_mongo_db_name_is_set_from_env(self) -> None:
        assert isinstance(TestingConfig.MONGO_DB_NAME, str)
        assert len(TestingConfig.MONGO_DB_NAME) > 0

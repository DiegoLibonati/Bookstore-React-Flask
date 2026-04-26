import pytest

from src.configs.default_config import DefaultConfig


@pytest.mark.unit
class TestDefaultConfig:
    def test_debug_is_false(self) -> None:
        assert DefaultConfig.DEBUG is False

    def test_testing_is_false(self) -> None:
        assert DefaultConfig.TESTING is False

    def test_json_as_ascii_is_false(self) -> None:
        assert DefaultConfig.JSON_AS_ASCII is False

    def test_mongo_uri_starts_with_mongodb_scheme(self) -> None:
        assert DefaultConfig.MONGO_URI.startswith("mongodb://")

    def test_mongo_uri_contains_auth_source(self) -> None:
        assert "authSource=" in DefaultConfig.MONGO_URI

    def test_mongo_auth_source_is_admin(self) -> None:
        assert DefaultConfig.MONGO_AUTH_SOURCE == "admin"

    def test_host_is_set(self) -> None:
        assert isinstance(DefaultConfig.HOST, str)
        assert len(DefaultConfig.HOST) > 0

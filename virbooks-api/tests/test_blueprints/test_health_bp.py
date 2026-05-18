from typing import Any

import pytest
from flask import Blueprint, Flask

from src.blueprints.v1.health_bp import health_bp


@pytest.fixture(scope="module")
def app_with_health_bp() -> Flask:
    app: Flask = Flask(__name__)
    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    return app


@pytest.mark.unit
class TestHealthBlueprintDefinition:
    def test_health_bp_is_blueprint_instance(self) -> None:
        assert isinstance(health_bp, Blueprint)

    def test_health_bp_has_correct_name(self) -> None:
        assert health_bp.name == "health"


@pytest.mark.unit
class TestHealthBlueprintRoutes:
    def test_root_route_is_registered(self, app_with_health_bp: Flask) -> None:
        rules: list[str] = [rule.rule for rule in app_with_health_bp.url_map.iter_rules()]
        assert "/api/v1/health/" in rules

    def test_root_route_supports_get(self, app_with_health_bp: Flask) -> None:
        rule_methods: dict[str, Any] = {rule.rule: rule.methods for rule in app_with_health_bp.url_map.iter_rules()}
        assert "GET" in rule_methods.get("/api/v1/health/", set())

    def test_root_route_does_not_support_post(self, app_with_health_bp: Flask) -> None:
        rule_methods: dict[str, Any] = {rule.rule: rule.methods for rule in app_with_health_bp.url_map.iter_rules()}
        assert "POST" not in rule_methods.get("/api/v1/health/", set())

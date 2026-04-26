from typing import Any

import pytest
from flask import Blueprint, Flask

from src.blueprints.v1.book_bp import book_bp


@pytest.fixture(scope="module")
def app_with_book_bp() -> Flask:
    app: Flask = Flask(__name__)
    app.register_blueprint(book_bp, url_prefix="/api/v1/books")
    return app


@pytest.mark.unit
class TestBookBlueprintDefinition:
    def test_book_bp_is_blueprint_instance(self) -> None:
        assert isinstance(book_bp, Blueprint)

    def test_book_bp_has_correct_name(self) -> None:
        assert book_bp.name == "book"


@pytest.mark.unit
class TestBookBlueprintRoutes:
    def test_alive_route_supports_get(self, app_with_book_bp: Flask) -> None:
        rule_methods: dict[str, Any] = {rule.rule: rule.methods for rule in app_with_book_bp.url_map.iter_rules()}
        assert "GET" in rule_methods.get("/api/v1/books/alive", set())

    def test_root_route_supports_get(self, app_with_book_bp: Flask) -> None:
        root_methods: set[str] = set()
        for rule in app_with_book_bp.url_map.iter_rules():
            if rule.rule == "/api/v1/books/":
                root_methods.update(rule.methods)
        assert "GET" in root_methods

    def test_root_route_supports_post(self, app_with_book_bp: Flask) -> None:
        root_methods: set[str] = set()
        for rule in app_with_book_bp.url_map.iter_rules():
            if rule.rule == "/api/v1/books/":
                root_methods.update(rule.methods)
        assert "POST" in root_methods

    def test_genres_route_supports_get(self, app_with_book_bp: Flask) -> None:
        rule_methods: dict[str, Any] = {rule.rule: rule.methods for rule in app_with_book_bp.url_map.iter_rules()}
        assert "GET" in rule_methods.get("/api/v1/books/genres", set())

    def test_variable_route_supports_get(self, app_with_book_bp: Flask) -> None:
        get_supported: bool = any("GET" in rule.methods for rule in app_with_book_bp.url_map.iter_rules() if "<" in rule.rule and "/api/v1/books" in rule.rule)
        assert get_supported

    def test_variable_route_supports_delete(self, app_with_book_bp: Flask) -> None:
        delete_supported: bool = any(
            "DELETE" in rule.methods for rule in app_with_book_bp.url_map.iter_rules() if "<" in rule.rule and "/api/v1/books" in rule.rule
        )
        assert delete_supported

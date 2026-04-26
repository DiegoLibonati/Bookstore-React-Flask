from typing import Any

import pytest
from flask import Flask

from src.blueprints.routes import register_routes


@pytest.fixture(scope="module")
def registered_app() -> Flask:
    app: Flask = Flask(__name__)
    register_routes(app)
    return app


@pytest.mark.unit
class TestRegisterRoutes:
    def test_book_blueprint_is_registered(self, registered_app: Flask) -> None:
        assert "book" in registered_app.blueprints

    def test_routes_are_prefixed_with_api_v1_books(self, registered_app: Flask) -> None:
        rules: list[str] = [rule.rule for rule in registered_app.url_map.iter_rules()]
        book_rules: list[str] = [r for r in rules if r.startswith("/api/v1/books")]
        assert len(book_rules) > 0

    def test_alive_route_is_registered(self, registered_app: Flask) -> None:
        rules: list[str] = [rule.rule for rule in registered_app.url_map.iter_rules()]
        assert "/api/v1/books/alive" in rules

    def test_root_route_is_registered(self, registered_app: Flask) -> None:
        rules: list[str] = [rule.rule for rule in registered_app.url_map.iter_rules()]
        assert "/api/v1/books/" in rules

    def test_genres_route_is_registered(self, registered_app: Flask) -> None:
        rules: list[str] = [rule.rule for rule in registered_app.url_map.iter_rules()]
        assert "/api/v1/books/genres" in rules

    def test_root_route_supports_get_and_post(self, registered_app: Flask) -> None:
        root_methods: set[str] = set()
        for rule in registered_app.url_map.iter_rules():
            if rule.rule == "/api/v1/books/":
                root_methods.update(rule.methods)
        assert "GET" in root_methods
        assert "POST" in root_methods

    def test_alive_route_supports_get(self, registered_app: Flask) -> None:
        rule_methods: dict[str, Any] = {rule.rule: rule.methods for rule in registered_app.url_map.iter_rules()}
        alive_methods: set[str] = rule_methods.get("/api/v1/books/alive", set())
        assert "GET" in alive_methods

    def test_genres_route_supports_get(self, registered_app: Flask) -> None:
        rule_methods: dict[str, Any] = {rule.rule: rule.methods for rule in registered_app.url_map.iter_rules()}
        genres_methods: set[str] = rule_methods.get("/api/v1/books/genres", set())
        assert "GET" in genres_methods

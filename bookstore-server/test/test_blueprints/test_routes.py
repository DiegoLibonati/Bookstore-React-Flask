from flask import Flask
from flask.testing import FlaskClient


class TestBlueprintRegistration:
    def test_book_blueprint_is_registered(self, app: Flask) -> None:
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert "book" in blueprint_names

    def test_routes_have_correct_prefix(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]

        book_routes = [rule for rule in rules if "/api/v1/books" in rule]
        assert len(book_routes) > 0, "No routes found with /api/v1/books prefix"

    def test_api_versioning_prefix_exists(self, app: Flask) -> None:
        rules = [rule.rule for rule in app.url_map.iter_rules()]

        versioned_routes = [rule for rule in rules if "/api/v1/" in rule]
        assert len(versioned_routes) > 0, "No versioned routes found"


class TestRoutesAccessibility:
    def test_books_endpoint_is_accessible(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/")

        assert response.status_code != 404

    def test_invalid_route_returns_404(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/nonexistent/")

        assert response.status_code == 404

    def test_wrong_api_version_returns_404(self, client: FlaskClient) -> None:
        response = client.get("/api/v2/books/")

        assert response.status_code == 404

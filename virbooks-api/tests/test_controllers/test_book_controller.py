from typing import Any

import pytest
from bson import ObjectId
from flask.testing import FlaskClient
from pymongo.database import Database

from src.constants.codes import (
    CODE_ALREADY_EXISTS_BOOK,
    CODE_NOT_FOUND_BOOK,
    CODE_SUCCESS_ADD_BOOK,
    CODE_SUCCESS_DELETE_BOOK,
    CODE_SUCCESS_GET_ALL_BOOKS,
    CODE_SUCCESS_GET_ALL_GENRES,
)

SAMPLE_BOOK: dict[str, str] = {
    "title": "Clean Code",
    "image": "https://example.com/image.jpg",
    "author": "Robert Martin",
    "description": "A handbook of agile software craftsmanship",
    "genre": "Technology",
}


@pytest.mark.integration
class TestAliveEndpoint:
    def test_returns_200_status(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")
        assert response.status_code == 200

    def test_returns_alive_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "I am Alive!"

    def test_returns_author_and_version_in_response(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")
        data: dict[str, Any] = response.get_json()
        assert "author" in data
        assert "version_bp" in data


@pytest.mark.integration
class TestGetBooksEndpoint:
    def test_returns_200_status(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/")
        assert response.status_code == 200

    def test_returns_success_code(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_GET_ALL_BOOKS

    def test_returns_empty_list_when_no_books(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/")
        data: dict[str, Any] = response.get_json()
        assert data["data"] == []

    def test_returns_books_when_they_exist(self, client: FlaskClient, mongo_db: Database) -> None:
        mongo_db.books.insert_one(SAMPLE_BOOK.copy())
        response = client.get("/api/v1/books/")
        data: dict[str, Any] = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["title"] == "Clean Code"


@pytest.mark.integration
class TestGetBooksByGenreEndpoint:
    def test_returns_200_status(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/Technology")
        assert response.status_code == 200

    def test_returns_books_matching_genre(self, client: FlaskClient, mongo_db: Database) -> None:
        mongo_db.books.insert_one(SAMPLE_BOOK.copy())
        mongo_db.books.insert_one({**SAMPLE_BOOK, "title": "Great Novel", "author": "Other", "genre": "Fiction"})
        response = client.get("/api/v1/books/Technology")
        data: dict[str, Any] = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["genre"] == "Technology"

    def test_returns_empty_list_when_genre_has_no_books(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/NonExistentGenre")
        data: dict[str, Any] = response.get_json()
        assert data["data"] == []


@pytest.mark.integration
class TestGetGenresEndpoint:
    def test_returns_200_status(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/genres")
        assert response.status_code == 200

    def test_returns_success_code(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/genres")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_GET_ALL_GENRES

    def test_returns_unique_genres(self, client: FlaskClient, mongo_db: Database) -> None:
        mongo_db.books.insert_one(SAMPLE_BOOK.copy())
        mongo_db.books.insert_one({**SAMPLE_BOOK, "title": "Novel", "author": "Other", "genre": "Fiction"})
        mongo_db.books.insert_one({**SAMPLE_BOOK, "title": "Tech 2", "author": "Another", "genre": "Technology"})
        response = client.get("/api/v1/books/genres")
        data: dict[str, Any] = response.get_json()
        assert set(data["data"]) == {"Technology", "Fiction"}

    def test_returns_empty_list_when_no_books(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.get("/api/v1/books/genres")
        data: dict[str, Any] = response.get_json()
        assert data["data"] == []


@pytest.mark.integration
class TestAddBookEndpoint:
    def test_returns_201_status(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        assert response.status_code == 201

    def test_returns_success_code(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_ADD_BOOK

    def test_returns_created_book_data_with_id(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        data: dict[str, Any] = response.get_json()
        assert "_id" in data["data"]
        assert data["data"]["title"] == "Clean Code"
        assert data["data"]["author"] == "Robert Martin"

    def test_returns_400_when_body_is_missing_required_fields(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/books/", json={})
        assert response.status_code == 400

    def test_returns_400_when_title_is_empty(self, client: FlaskClient, mongo_db: Database) -> None:
        response = client.post("/api/v1/books/", json={**SAMPLE_BOOK, "title": ""})
        assert response.status_code == 400

    def test_returns_409_when_book_already_exists(self, client: FlaskClient, mongo_db: Database) -> None:
        client.post("/api/v1/books/", json=SAMPLE_BOOK)
        response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        assert response.status_code == 409
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_ALREADY_EXISTS_BOOK


@pytest.mark.integration
class TestDeleteBookEndpoint:
    def test_returns_200_status_when_book_exists(self, client: FlaskClient, mongo_db: Database) -> None:
        add_response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        book_id: str = add_response.get_json()["data"]["_id"]
        response = client.delete(f"/api/v1/books/{book_id}")
        assert response.status_code == 200

    def test_returns_success_code_after_deletion(self, client: FlaskClient, mongo_db: Database) -> None:
        add_response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        book_id: str = add_response.get_json()["data"]["_id"]
        response = client.delete(f"/api/v1/books/{book_id}")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_DELETE_BOOK

    def test_book_is_removed_from_database_after_deletion(self, client: FlaskClient, mongo_db: Database) -> None:
        add_response = client.post("/api/v1/books/", json=SAMPLE_BOOK)
        book_id: str = add_response.get_json()["data"]["_id"]
        client.delete(f"/api/v1/books/{book_id}")
        get_response = client.get("/api/v1/books/")
        data: dict[str, Any] = get_response.get_json()
        assert data["data"] == []

    def test_returns_404_when_book_does_not_exist(self, client: FlaskClient, mongo_db: Database) -> None:
        fake_id: str = str(ObjectId())
        response = client.delete(f"/api/v1/books/{fake_id}")
        assert response.status_code == 404
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_NOT_FOUND_BOOK

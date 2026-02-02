from bson import ObjectId
from flask import Flask
from flask.testing import FlaskClient
from pymongo.database import Database

from src.constants.codes import (
    CODE_SUCCESS_ADD_BOOK,
    CODE_SUCCESS_DELETE_BOOK,
    CODE_SUCCESS_GET_ALL_BOOKS,
    CODE_SUCCESS_GET_ALL_GENRES,
)


class TestAliveEndpoint:
    def test_alive_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")

        assert response.status_code == 200

    def test_alive_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")
        data = response.get_json()

        assert "message" in data
        assert "version_bp" in data
        assert "author" in data
        assert "name_bp" in data

    def test_alive_returns_correct_values(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")
        data = response.get_json()

        assert data["message"] == "I am Alive!"
        assert data["version_bp"] == "2.0.0"
        assert data["author"] == "Diego Libonati"
        assert data["name_bp"] == "Books"

    def test_alive_returns_json_content_type(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/alive")

        assert response.content_type == "application/json"


class TestGetBooksEndpoint:
    def test_get_books_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/")

        assert response.status_code == 200

    def test_get_books_returns_empty_list_when_no_books(
        self, app: Flask, client: FlaskClient, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        response = client.get("/api/v1/books/")
        data = response.get_json()

        assert data["data"] == []

    def test_get_books_returns_all_books(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/books/")
        data = response.get_json()

        assert len(data["data"]) == len(inserted_books)

    def test_get_books_returns_correct_structure(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_get_books_returns_correct_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_ALL_BOOKS


class TestGetBooksByGenreEndpoint:
    def test_get_books_by_genre_returns_200(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/books/Test")

        assert response.status_code == 200

    def test_get_books_by_genre_filters_correctly(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/books/Test")
        data = response.get_json()

        # All inserted_books have genre "Test"
        assert len(data["data"]) == len(inserted_books)

    def test_get_books_by_genre_returns_empty_for_nonexistent_genre(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/books/NonExistentGenre")
        data = response.get_json()

        assert data["data"] == []

    def test_get_books_by_genre_returns_correct_structure(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/books/Test")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data


class TestAddBookEndpoint:
    def test_add_book_returns_201(
        self, client: FlaskClient, sample_book: dict[str, str]
    ) -> None:
        response = client.post("/api/v1/books/", json=sample_book)

        assert response.status_code == 201

    def test_add_book_creates_book_in_database(
        self, client: FlaskClient, sample_book: dict[str, str], mongo_db: Database
    ) -> None:
        initial_count = mongo_db.books.count_documents({})

        client.post("/api/v1/books/", json=sample_book)

        final_count = mongo_db.books.count_documents({})
        assert final_count == initial_count + 1

    def test_add_book_returns_created_book_data(
        self, client: FlaskClient, sample_book: dict[str, str]
    ) -> None:
        response = client.post("/api/v1/books/", json=sample_book)
        data = response.get_json()

        assert "_id" in data["data"]
        assert data["data"]["title"] == sample_book["title"]
        assert data["data"]["author"] == sample_book["author"]

    def test_add_book_returns_correct_structure(
        self, client: FlaskClient, sample_book: dict[str, str]
    ) -> None:
        response = client.post("/api/v1/books/", json=sample_book)
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_add_book_returns_correct_code(
        self, client: FlaskClient, sample_book: dict[str, str]
    ) -> None:
        response = client.post("/api/v1/books/", json=sample_book)
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_ADD_BOOK

    def test_add_book_with_invalid_data_returns_400(self, client: FlaskClient) -> None:
        invalid_book = {"title": "Only Title"}

        response = client.post("/api/v1/books/", json=invalid_book)

        assert response.status_code == 400

    def test_add_book_without_body_returns_error(self, client: FlaskClient) -> None:
        response = client.post("/api/v1/books/", json={})

        assert response.status_code in [400, 422, 500]


class TestDeleteBookEndpoint:
    def test_delete_book_returns_200(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        book_id = inserted_books[0]["_id"]

        response = client.delete(f"/api/v1/books/{book_id}")

        assert response.status_code == 200

    def test_delete_book_removes_from_database(
        self,
        client: FlaskClient,
        inserted_books: list[dict[str, str]],
        mongo_db: Database,
    ) -> None:
        book_id = inserted_books[0]["_id"]
        initial_count = mongo_db.books.count_documents({})

        client.delete(f"/api/v1/books/{book_id}")

        final_count = mongo_db.books.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_book_returns_correct_structure(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        book_id = inserted_books[0]["_id"]

        response = client.delete(f"/api/v1/books/{book_id}")
        data = response.get_json()

        assert "code" in data
        assert "message" in data

    def test_delete_book_returns_correct_code(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        book_id = inserted_books[0]["_id"]

        response = client.delete(f"/api/v1/books/{book_id}")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_DELETE_BOOK

    def test_delete_nonexistent_book_returns_404(self, client: FlaskClient) -> None:
        fake_id = str(ObjectId())

        response = client.delete(f"/api/v1/books/{fake_id}")

        assert response.status_code == 404


class TestGetAllGenresEndpoint:
    def test_get_all_genres_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/genres")

        assert response.status_code == 200

    def test_get_all_genres_returns_correct_structure(
        self, client: FlaskClient
    ) -> None:
        response = client.get("/api/v1/books/genres")
        data = response.get_json()

        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_get_all_genres_returns_list(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/genres")
        data = response.get_json()

        assert isinstance(data["data"], list)

    def test_get_all_genres_returns_correct_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/books/genres")
        data = response.get_json()

        assert data["code"] == CODE_SUCCESS_GET_ALL_GENRES

    def test_get_all_genres_returns_unique_genres(
        self, client: FlaskClient, inserted_books: list[dict[str, str]]
    ) -> None:
        response = client.get("/api/v1/books/genres")
        data = response.get_json()

        assert "Test" in data["data"]

from test.constants import BLUEPRINTS
from unittest.mock import MagicMock, patch

from bson import ObjectId
from flask.testing import FlaskClient

from src.constants.codes import (
    CODE_SUCCESS_ADD_BOOK,
    CODE_SUCCESS_DELETE_BOOK,
    CODE_SUCCESS_GET_ALL_BOOKS,
    CODE_SUCCESS_GET_ALL_GENRES,
)
from src.constants.messages import (
    MESSAGE_SUCCESS_ADD_BOOK,
    MESSAGE_SUCCESS_DELETE_BOOK,
    MESSAGE_SUCCESS_GET_ALL_BOOKS,
    MESSAGE_SUCCESS_GET_ALL_GENRES,
)


def test_alive(flask_client: FlaskClient) -> None:
    response = flask_client.get(f"{BLUEPRINTS.get('books')}/alive")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "I am Alive!"
    assert data["version_bp"] == "2.0.0"
    assert data["author"] == "Diego Libonati"
    assert data["name_bp"] == "Books"


def test_add_book_success(
    flask_client: FlaskClient, dracula_book: dict[str, str]
) -> None:
    mock_inserted_id = ObjectId()
    mock_result = MagicMock(inserted_id=mock_inserted_id)

    with patch(
        "src.controllers.book_controller.BookService.add_book", return_value=mock_result
    ):
        response = flask_client.post(f"{BLUEPRINTS.get('books')}/", json=dracula_book)

    assert response.status_code == 201
    data = response.get_json()
    assert data["code"] == CODE_SUCCESS_ADD_BOOK
    assert data["message"] == MESSAGE_SUCCESS_ADD_BOOK
    assert data["data"]["_id"] == str(mock_inserted_id)
    assert data["data"]["title"] == dracula_book["title"]


def test_get_books(flask_client: FlaskClient) -> None:
    fake_books = [{"_id": "1", "title": "Book1"}, {"_id": "2", "title": "Book2"}]
    with patch(
        "src.controllers.book_controller.BookService.get_all_books",
        return_value=fake_books,
    ):
        response = flask_client.get(f"{BLUEPRINTS.get('books')}/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == CODE_SUCCESS_GET_ALL_BOOKS
    assert data["message"] == MESSAGE_SUCCESS_GET_ALL_BOOKS
    assert data["data"] == fake_books


def test_get_books_by_genre(flask_client: FlaskClient) -> None:
    fake_books = [{"_id": "1", "title": "Dracula", "genre": "Horror"}]
    with patch(
        "src.controllers.book_controller.BookService.get_all_books_by_genre",
        return_value=fake_books,
    ):
        response = flask_client.get(f"{BLUEPRINTS.get('books')}/Horror")

    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == CODE_SUCCESS_GET_ALL_BOOKS
    assert data["message"] == MESSAGE_SUCCESS_GET_ALL_BOOKS
    assert data["data"][0]["genre"] == "Horror"


def test_delete_book(flask_client: FlaskClient) -> None:
    with patch(
        "src.controllers.book_controller.BookService.delete_book_by_id",
        return_value=None,
    ) as mock_delete:
        response = flask_client.delete(f"{BLUEPRINTS.get('books')}/123")

    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == CODE_SUCCESS_DELETE_BOOK
    assert data["message"] == MESSAGE_SUCCESS_DELETE_BOOK
    mock_delete.assert_called_once_with("123")


def test_get_all_genres(flask_client: FlaskClient) -> None:
    fake_genres = ["Horror", "Fantasy"]
    with patch(
        "src.controllers.book_controller.BookService.get_all_genres",
        return_value=fake_genres,
    ):
        response = flask_client.get(f"{BLUEPRINTS.get('books')}/genres")

    assert response.status_code == 200
    data = response.get_json()
    assert data["code"] == CODE_SUCCESS_GET_ALL_GENRES
    assert data["message"] == MESSAGE_SUCCESS_GET_ALL_GENRES
    assert set(data["data"]) == {"Horror", "Fantasy"}

from unittest.mock import patch

import pytest
from bson import ObjectId

from src.constants.codes import CODE_ERROR_BOOK_ALREADY_EXISTS, CODE_NOT_FOUND_BOOK
from src.constants.messages import (
    MESSAGE_ERROR_BOOK_ALREADY_EXISTS,
    MESSAGE_NOT_FOUND_BOOK,
)
from src.models.book_model import BookModel
from src.services.book_service import BookService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


def test_add_book_success(book_model: BookModel) -> None:
    with patch(
        "src.services.book_service.BookDAO.find_one_by_title_and_author",
        return_value=None,
    ), patch(
        "src.services.book_service.BookDAO.insert_one", return_value="mocked_result"
    ) as mock_insert:
        result = BookService.add_book(book_model)
        assert result == "mocked_result"
        mock_insert.assert_called_once_with(book_model.model_dump())


def test_add_book_already_exists(book_model: BookModel) -> None:
    with patch(
        "src.services.book_service.BookDAO.find_one_by_title_and_author",
        return_value={"title": "Drácula"},
    ):
        with pytest.raises(ConflictAPIError) as exc:
            BookService.add_book(book_model)
        assert exc.value.code == CODE_ERROR_BOOK_ALREADY_EXISTS
        assert exc.value.message == MESSAGE_ERROR_BOOK_ALREADY_EXISTS


def test_get_all_books_returns_list() -> None:
    fake_books = [{"title": "Book1"}, {"title": "Book2"}]
    with patch("src.services.book_service.BookDAO.find", return_value=fake_books):
        result = BookService.get_all_books()
        assert result == fake_books


def test_get_all_books_by_genre_returns_list() -> None:
    fake_books = [{"title": "Book1", "genre": "Horror"}]
    with patch(
        "src.services.book_service.BookDAO.find_by_genre", return_value=fake_books
    ):
        result = BookService.get_all_books_by_genre("Horror")
        assert result == fake_books


def test_get_all_genres_unique_list() -> None:
    fake_books = [
        {"title": "Book1", "genre": "Horror"},
        {"title": "Book2", "genre": "Fantasy"},
        {"title": "Book3", "genre": "Horror"},
        {"title": "Book4"},
    ]
    with patch("src.services.book_service.BookDAO.find", return_value=fake_books):
        result = BookService.get_all_genres()
        assert set(result) == {"Horror", "Fantasy"}


def test_delete_book_by_id_success() -> None:
    _id = ObjectId()
    with patch(
        "src.services.book_service.BookDAO.find_by_id", return_value={"_id": _id}
    ), patch(
        "src.services.book_service.BookDAO.delete_one_by_id", return_value="deleted"
    ) as mock_delete:
        result = BookService.delete_book_by_id(_id)
        assert result == "deleted"
        mock_delete.assert_called_once_with(_id)


def test_delete_book_by_id_not_found() -> None:
    _id = ObjectId()
    with patch("src.services.book_service.BookDAO.find_by_id", return_value=None):
        with pytest.raises(NotFoundAPIError) as exc:
            BookService.delete_book_by_id(_id)
        assert exc.value.code == CODE_NOT_FOUND_BOOK
        assert exc.value.message == MESSAGE_NOT_FOUND_BOOK

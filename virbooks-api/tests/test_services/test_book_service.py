from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.models.book_model import BookModel
from src.services.book_service import BookService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError

VALID_BOOK_DATA: dict[str, str] = {
    "title": "Clean Code",
    "image": "https://example.com/image.jpg",
    "author": "Robert Martin",
    "description": "A handbook of agile software craftsmanship",
    "genre": "Technology",
}


@pytest.mark.unit
class TestBookServiceAddBook:
    def test_add_book_calls_insert_when_book_does_not_exist(self) -> None:
        book: BookModel = BookModel(**VALID_BOOK_DATA)
        mock_result: MagicMock = MagicMock(spec=InsertOneResult)
        mock_result.inserted_id = ObjectId()

        with (
            patch("src.services.book_service.BookDAO.find_one_by_title_and_author", return_value=None),
            patch("src.services.book_service.BookDAO.insert_one", return_value=mock_result) as mock_insert,
        ):
            result: InsertOneResult = BookService.add_book(book=book)

        mock_insert.assert_called_once_with(book.model_dump())
        assert result.inserted_id is not None

    def test_add_book_raises_conflict_when_book_already_exists(self) -> None:
        book: BookModel = BookModel(**VALID_BOOK_DATA)
        existing_book: dict[str, str] = {"title": "Clean Code", "author": "Robert Martin"}

        with patch("src.services.book_service.BookDAO.find_one_by_title_and_author", return_value=existing_book):
            with pytest.raises(ConflictAPIError):
                BookService.add_book(book=book)


@pytest.mark.unit
class TestBookServiceGetAllBooks:
    def test_get_all_books_returns_list_of_books(self) -> None:
        mock_books: list[dict[str, Any]] = [
            {"_id": "1", "title": "Book One", "author": "A", "image": "i", "description": "d", "genre": "Fiction"},
        ]

        with patch("src.services.book_service.BookDAO.find", return_value=mock_books):
            result: list[dict[str, Any]] = BookService.get_all_books()

        assert result == mock_books

    def test_get_all_books_returns_empty_list_when_no_books(self) -> None:
        with patch("src.services.book_service.BookDAO.find", return_value=[]):
            result: list[dict[str, Any]] = BookService.get_all_books()

        assert result == []


@pytest.mark.unit
class TestBookServiceGetAllBooksByGenre:
    def test_get_all_books_by_genre_calls_dao_with_correct_genre(self) -> None:
        mock_books: list[dict[str, Any]] = [
            {"_id": "1", "title": "Tech Book", "genre": "Technology"},
        ]

        with patch("src.services.book_service.BookDAO.find_by_genre", return_value=mock_books) as mock_find:
            result: list[dict[str, Any]] = BookService.get_all_books_by_genre("Technology")

        mock_find.assert_called_once_with("Technology")
        assert result == mock_books

    def test_get_all_books_by_genre_returns_empty_list_when_no_match(self) -> None:
        with patch("src.services.book_service.BookDAO.find_by_genre", return_value=[]):
            result: list[dict[str, Any]] = BookService.get_all_books_by_genre("NonExistentGenre")

        assert result == []


@pytest.mark.unit
class TestBookServiceGetAllGenres:
    def test_get_all_genres_returns_unique_genres(self) -> None:
        mock_books: list[dict[str, Any]] = [
            {"genre": "Technology"},
            {"genre": "Fiction"},
            {"genre": "Technology"},
        ]

        with patch("src.services.book_service.BookDAO.find", return_value=mock_books):
            result: list[str] = BookService.get_all_genres()

        assert set(result) == {"Technology", "Fiction"}
        assert len(result) == 2

    def test_get_all_genres_returns_empty_list_when_no_books(self) -> None:
        with patch("src.services.book_service.BookDAO.find", return_value=[]):
            result: list[str] = BookService.get_all_genres()

        assert result == []

    def test_get_all_genres_skips_books_without_genre_field(self) -> None:
        mock_books: list[dict[str, Any]] = [
            {"genre": "Technology"},
            {"title": "Book Without Genre"},
            {"genre": ""},
        ]

        with patch("src.services.book_service.BookDAO.find", return_value=mock_books):
            result: list[str] = BookService.get_all_genres()

        assert result == ["Technology"]


@pytest.mark.unit
class TestBookServiceDeleteBookById:
    def test_delete_book_calls_dao_delete_when_book_exists(self) -> None:
        book_id: str = str(ObjectId())
        existing_book: dict[str, str] = {"_id": book_id, "title": "Clean Code"}
        mock_delete_result: MagicMock = MagicMock(spec=DeleteResult)

        with (
            patch("src.services.book_service.BookDAO.find_one_by_id", return_value=existing_book),
            patch("src.services.book_service.BookDAO.delete_one_by_id", return_value=mock_delete_result) as mock_del,
        ):
            result: DeleteResult = BookService.delete_book_by_id(book_id)

        mock_del.assert_called_once_with(book_id)
        assert result is mock_delete_result

    def test_delete_book_raises_not_found_when_book_does_not_exist(self) -> None:
        book_id: str = str(ObjectId())

        with patch("src.services.book_service.BookDAO.find_one_by_id", return_value=None):
            with pytest.raises(NotFoundAPIError):
                BookService.delete_book_by_id(book_id)

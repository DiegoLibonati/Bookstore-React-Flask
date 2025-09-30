from typing import Any

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import CODE_ERROR_BOOK_ALREADY_EXISTS, CODE_NOT_FOUND_BOOK
from src.constants.messages import (
    MESSAGE_ERROR_BOOK_ALREADY_EXISTS,
    MESSAGE_NOT_FOUND_BOOK,
)
from src.data_access.book_dao import BookDAO
from src.models.book_model import BookModel
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class BookService:
    @staticmethod
    def add_book(book: BookModel) -> InsertOneResult:
        existing = BookDAO.find_one_by_title_and_author(book.title, book.author)
        if existing:
            raise ConflictAPIError(
                code=CODE_ERROR_BOOK_ALREADY_EXISTS,
                message=MESSAGE_ERROR_BOOK_ALREADY_EXISTS,
            )
        return BookDAO.insert_one(book.model_dump())

    @staticmethod
    def get_all_books() -> list[dict[str, Any]]:
        return BookDAO.find()

    @staticmethod
    def get_all_books_by_genre(genre: str) -> list[dict[str, Any]]:
        return BookDAO.find_by_genre(genre)

    @staticmethod
    def get_all_genres() -> list[str]:
        books = BookDAO.find()

        genres = {book.get("genre") for book in books if book.get("genre")}
        return list(genres)

    @staticmethod
    def delete_book_by_id(_id: ObjectId) -> DeleteResult:
        existing = BookDAO.find_one_by_id(_id)

        if not existing:
            raise NotFoundAPIError(
                code=CODE_NOT_FOUND_BOOK, message=MESSAGE_NOT_FOUND_BOOK
            )

        return BookDAO.delete_one_by_id(_id)

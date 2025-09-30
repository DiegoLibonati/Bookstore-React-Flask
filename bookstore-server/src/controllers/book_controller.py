from flask import Response, jsonify, request

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
from src.models.book_model import BookModel
from src.services.book_service import BookService
from src.utils.error_handler import handle_exceptions


@handle_exceptions
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Books",
    }

    return jsonify(response), 200


@handle_exceptions
def add_book() -> Response:
    body = request.json
    book = BookModel(**body)

    result = BookService.add_book(book=book)

    data = {"_id": str(result.inserted_id), **book.model_dump()}

    response = {
        "code": CODE_SUCCESS_ADD_BOOK,
        "message": MESSAGE_SUCCESS_ADD_BOOK,
        "data": data,
    }

    return jsonify(response), 201


@handle_exceptions
def get_books() -> Response:
    books = BookService.get_all_books()

    response = {
        "code": CODE_SUCCESS_GET_ALL_BOOKS,
        "message": MESSAGE_SUCCESS_GET_ALL_BOOKS,
        "data": books,
    }

    return jsonify(response), 200


@handle_exceptions
def get_books_by_genre(genre: str) -> Response:
    books = BookService.get_all_books_by_genre(genre)

    response = {
        "code": CODE_SUCCESS_GET_ALL_BOOKS,
        "message": MESSAGE_SUCCESS_GET_ALL_BOOKS,
        "data": books,
    }

    return jsonify(response), 200


@handle_exceptions
def delete_book(id: str) -> Response:
    BookService.delete_book_by_id(id)

    response = {
        "code": CODE_SUCCESS_DELETE_BOOK,
        "message": MESSAGE_SUCCESS_DELETE_BOOK,
    }

    return jsonify(response), 200


@handle_exceptions
def get_all_genres() -> Response:
    genres = BookService.get_all_genres()

    response = {
        "code": CODE_SUCCESS_GET_ALL_GENRES,
        "message": MESSAGE_SUCCESS_GET_ALL_GENRES,
        "data": genres,
    }

    return jsonify(response), 200

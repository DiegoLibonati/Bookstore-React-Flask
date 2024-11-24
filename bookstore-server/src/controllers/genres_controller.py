from typing import Any

from flask import make_response
from flask import current_app

from src.data_access.books_repository import BookRepository


def alive_genres() -> dict[str, Any]:
    return make_response({
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Genres"
    }, 200)


def get_all_genres() -> dict[str, Any]:
    books = BookRepository(db=current_app.mongo.db).get_genres()

    return make_response({
        "message": "The book genres were successfully obtained.",
        "data": books
    }, 200)

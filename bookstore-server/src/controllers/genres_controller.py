from flask import make_response
from flask import current_app
from flask import Response


def alive_genres() -> Response:
    return make_response({
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Genres"
    }, 200)


def get_all_genres() -> Response:
    books = current_app.book_repository.get_genres()

    return make_response({
        "message": "The book genres were successfully obtained.",
        "data": books
    }, 200)

from typing import Any
from bson import json_util

from flask import make_response
from flask import current_app


def alive_genres() -> dict[str, Any]:
    return make_response({
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Genres"
    }, 200)


def get_all_genres() -> dict[str, Any]:
    books = current_app.mongo.db.books.distinct("genre")

    data = json_util.loads(json_util.dumps(books))

    return make_response({
        "message": "The book genres were successfully obtained.",
        "data": data
    }, 200)

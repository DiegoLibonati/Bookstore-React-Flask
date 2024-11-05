from typing import Any
from bson import ObjectId

from flask import make_response
from flask import current_app
from flask import request

from utils.utils import parse_books


def get_books() -> dict[str, Any]:
    books = current_app.mongo.db.books.find()

    data = parse_books(books=books)

    return make_response({
        "message": "Books were successfully obtained.",
        "data": data
    }, 200)


def get_books_by_genre(genre: str) -> dict[str, Any]:
    books = current_app.mongo.db.books.find({
        "genre" : genre
    })

    data = parse_books(books=books)
    
    return make_response({
        "message": "Books were successfully obtained.",
        "data": data
    }, 200)


def add_book() -> dict[str, Any]:
    image = request.json['image']
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    genre = request.json['genre']

    book = {
        'title':title,
        'author': author,
        'description': description,
        'image': image,
        'genre': genre,
    }

    if not image or not title or not author or not description or not genre:
        return make_response({
            "message": "The requested book could not be added.",
            "fields": book,
            "data": None
        }, 400)

    insert_result = current_app.mongo.db.books.insert_one(book)
    book['_id'] = str(insert_result.inserted_id)

    return make_response({
        "message": "The book was successfully added.",
        "data": book
    }, 201)
    

def delete_book(id: str) -> dict[str, Any]:
    try:
        current_app.mongo.db.books.delete_one({
            "_id": ObjectId(id)
        })

        return make_response({
            "message": f"{id} was deleted."
        }, 200)
    except Exception as e:
        return make_response({
            "message": str(e)
        }, 400)
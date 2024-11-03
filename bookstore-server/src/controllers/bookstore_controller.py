from typing import Any
from bson import json_util, ObjectId

from flask import make_response, current_app, request

from utils.utils import not_accepted


def get_books() -> dict[str, Any]:
    books = current_app.mongo.db.books.find()

    data = [{**book, "_id": str(book["_id"])} for book in books]

    return make_response({
        "message": "Books were successfully obtained.",
        "data": data
    }, 200)


def get_books_by_genre(genre: str) -> dict[str, Any]:
    books = current_app.mongo.db.books.find({
        "genre" : genre
    })

    data = [{**book, "_id": str(book["_id"])} for book in books]
    
    return make_response({
        "message": "Books were successfully obtained.",
        "data": data
    }, 200)


def get_all_genres() -> dict[str, Any]:
    books = current_app.mongo.db.books.distinct("genre")

    data = json_util.loads(json_util.dumps(books))

    return make_response({
        "message": "The book genres were successfully obtained.",
        "data": data
    }, 200)


def add_book() -> dict[str, Any]:
    image = request.json['image']
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    genre = request.json['genre']

    if not image or not title or not author or not description or not genre: return not_accepted()

    response = {
        'title':title,
        'author': author,
        'description': description,
        'image': image,
        'genre': genre,
    }

    insert_result = current_app.mongo.db.books.insert_one(response)
    response['_id'] = str(insert_result.inserted_id)

    return make_response({
        "message": "The book was successfully added.",
        "data": response
    }, 201)
    

def delete_book(id: str) -> dict[str, Any]:
    current_app.mongo.db.books.delete_one({
        "_id": ObjectId(id)
    })

    return make_response({
        "message": f"{id} was deleted"
    }, 200)
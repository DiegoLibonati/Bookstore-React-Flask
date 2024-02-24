from flask import make_response, current_app, request
from bson import json_util, ObjectId
from utils.utils import not_accepted


def get_books() -> tuple:
    books = current_app.mongo.db.libros.find()

    response = json_util.dumps(books)

    return make_response(
        response, 
    200)


def get_books_by_genre(genre: str) -> tuple:
    books = current_app.mongo.db.libros.find({
        "genre" : genre
    })

    response = json_util.dumps(books)

    return make_response(
        response, 
    200)


def get_all_genres() -> tuple:
    books = current_app.mongo.db.libros.distinct("genre")

    response = json_util.dumps(books)

    return make_response(
        response, 
    200)


def add_book() -> tuple:
    image = request.json['image']
    title = request.json['title']
    author = request.json['author']
    description = request.json['description']
    genre = request.json['genre']

    if (image and title and author and description and genre) and (image.isspace() == False and title.isspace() == False and author.isspace() == False and description.isspace() == False and genre.isspace() == False):
        
        response = {
            'title':title,
            'author': author,
            'description': description,
            'image': image,
            'genre': genre,
        }

        current_app.mongo.db.libros.insert_one(response)

        return make_response(
            f"Added: {response}",
        201)
    else:
        return not_accepted()
    

def delete_book(id: str) -> tuple:
    current_app.mongo.db.libros.delete_one(
        {"_id": ObjectId(id)}
    )

    response = f"{id} was deleted"

    return make_response(
        response,
    200)
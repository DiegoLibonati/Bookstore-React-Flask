from typing import Any
from bson import ObjectId

from flask import make_response
from flask import current_app
from flask import request

from src.models.Book import Book
from src.models.BookManager import BookManager


def alive_books() -> dict[str, Any]:
    return make_response({
        "message": "I am Alive!",
        "version_bp": "2.0.0",
        "author": "Diego Libonati",
        "name_bp": "Books"
    }, 200)


def get_books() -> dict[str, Any]:
    book_manager = BookManager()
    books = current_app.book_repository.get_all_books()

    book_manager.add_books(books=books)
    
    data = book_manager.parse_items()

    return make_response({
        "message": "Books were successfully obtained.",
        "data": data
    }, 200)


def get_books_by_genre(genre: str) -> dict[str, Any]:
    book_manager = BookManager()
    books = current_app.book_repository.get_books_by_genre(genre=genre)

    book_manager.add_books(books=books)
    
    data = book_manager.parse_items()
    
    return make_response({
        "message": "Books were successfully obtained.",
        "data": data
    }, 200)


def add_book() -> dict[str, Any]:
    image = request.json.get('image', "").strip()
    title = request.json.get('title', "").strip()
    author = request.json.get('author', "").strip()
    description = request.json.get('description', "").strip()
    genre = request.json.get('genre', "").strip()

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
            "data": None
        }, 400)

    id_inserted = current_app.book_repository.insert_book(book=book)
    book["_id"] = id_inserted

    book = Book(**book)

    return make_response({
        "message": "The book was successfully added.",
        "data": book.to_dict()
    }, 201)
    

def delete_book(id: str) -> dict[str, Any]:
    try:
        object_id = ObjectId(id)
        document = current_app.book_repository.get_book_by_id(book_id=object_id)

        if not document: 
            return make_response({
                "message": f"No book found with id: {id}.",
                "data": None
            }, 404)
        
        book = Book(**document)

        current_app.book_repository.delete_book_by_id(book_id=book.id)

        return make_response({
            "message": f"Book with id: {id} was deleted.",
            "data": book.to_dict()
        }, 200)
    except Exception as e: 
        return make_response({
            "message": f"Error deleting book: {str(e)}"
        }, 400)
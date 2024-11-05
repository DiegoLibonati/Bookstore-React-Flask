from typing import Any

from flask import Blueprint

from controllers import bookstore_controller


bookstore_route = Blueprint("bookstore_route", __name__)


@bookstore_route.route('/books', methods = ['GET'])
def get_books() -> dict[str, Any]:
    return bookstore_controller.get_books()


@bookstore_route.route('/books/add', methods=["POST"])
def add_book() -> dict[str, Any]:
    return bookstore_controller.add_book()


@bookstore_route.route('/books/delete/<id>', methods=['DELETE'])
def delete_book(id: str) -> dict[str, Any]:
    return bookstore_controller.delete_book(id)


@bookstore_route.route('/genres', methods=['GET'])
def get_all_genres() -> dict[str, Any]:
   return bookstore_controller.get_all_genres()


@bookstore_route.route('/genres/<genre>', methods = ['GET'])
def get_books_by_genre(genre: str) -> dict[str, Any]:
    return bookstore_controller.get_books_by_genre(genre)
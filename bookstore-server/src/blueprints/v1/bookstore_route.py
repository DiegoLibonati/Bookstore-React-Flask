from flask import Blueprint
from flask_cors import cross_origin

from controllers import bookstore_controller


bookstore_route = Blueprint("bookstore_route", __name__)


@bookstore_route.route('/', methods = ['GET'])
@cross_origin()
def get_books() -> tuple:
    return bookstore_controller.get_books()


@bookstore_route.route('/<genre>', methods = ['GET'])
@cross_origin()
def get_books_by_genre(genre: str) -> tuple:
    return bookstore_controller.get_books_by_genre(genre)


@bookstore_route.route('/genres', methods=['GET'])
@cross_origin()
def get_all_genres() -> tuple:
   return bookstore_controller.get_all_genres()


@bookstore_route.route('/add', methods=["POST"])
def add_book() -> tuple:
    return bookstore_controller.add_book()


@bookstore_route.route('/<id>', methods=['DELETE'])
def delete_book(id: str) -> tuple:
    return bookstore_controller.delete_book(id)
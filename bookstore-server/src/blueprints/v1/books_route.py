from flask import Blueprint
from flask import Response

from src.controllers import books_controller


books_route = Blueprint("books_route", __name__)


@books_route.route('/alive', methods = ['GET'])
def alive_books() -> Response:
    return books_controller.alive_books()


@books_route.route('/', methods = ['GET'])
def get_books() -> Response:
    return books_controller.get_books()


@books_route.route('/<genre>', methods = ['GET'])
def get_books_by_genre(genre: str) -> Response:
    return books_controller.get_books_by_genre(genre)


@books_route.route('/add', methods=["POST"])
def add_book() -> Response:
    return books_controller.add_book()


@books_route.route('/delete/<id>', methods=['DELETE'])
def delete_book(id: str) -> Response:
    return books_controller.delete_book(id)

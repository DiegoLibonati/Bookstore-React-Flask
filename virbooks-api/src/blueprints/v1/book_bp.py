from flask import Blueprint

from src.controllers.book_controller import (
    add_book,
    alive,
    delete_book,
    get_all_genres,
    get_books,
    get_books_by_genre,
)

book_bp = Blueprint("book", __name__)

book_bp.route("/alive", methods=["GET"])(alive)
book_bp.route("/", methods=["GET"])(get_books)
book_bp.route("/<genre>", methods=["GET"])(get_books_by_genre)
book_bp.route("/genres", methods=["GET"])(get_all_genres)
book_bp.route("/", methods=["POST"])(add_book)
book_bp.route("/<id>", methods=["DELETE"])(delete_book)

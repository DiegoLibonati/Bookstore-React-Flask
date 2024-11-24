import logging

import pytest

from src.models.Book import Book
from src.models.BookManager import BookManager


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_init_book_manager(book_manager_model: BookManager, book_test: dict[str, str]) -> None:
    assert book_manager_model
    assert not book_manager_model.books
    assert book_manager_model.initializer(**book_test)

def test_add_book(book_manager_model: BookManager, book_model: Book) -> None:
    book_manager_model.add_book(book=book_model)

    assert book_manager_model.books
    assert book_model in book_manager_model.books

def test_add_book_with_wrong_book(book_manager_model: BookManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        book_manager_model.add_book(book={"pepe": "123"})

    assert str(exc_info.value) == "You must enter a valid book in order to add it."

def test_add_books(book_manager_model: BookManager, book_test: dict[str, str]) -> None:
    book_manager_model.add_books(books=[book_test])

    assert book_manager_model.books
    assert book_test in book_manager_model.parse_items()

def test_add_books_with_wrong_books(book_manager_model: BookManager) -> None:
    with pytest.raises(TypeError) as exc_info:
        book_manager_model.add_books(books={})

    assert str(exc_info.value) == "You must enter a valid books to add its."

def test_parse_books(book_manager_model: BookManager) -> None:
    parsed_books = book_manager_model.parse_items()

    assert isinstance(parsed_books, list)

    for book in parsed_books:
        assert isinstance(book, dict)
        assert book.get("_id")
        assert book.get("title")
        assert book.get("image")
        assert book.get("description")
        assert book.get("author")
        assert book.get("genre")
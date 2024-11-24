from bson import ObjectId

import pytest

from src.data_access.books_repository import BookRepository


@pytest.mark.usefixtures("mongo_test_db")
def test_get_all_books(book_repository: BookRepository) -> None:
    books = book_repository.get_all_books()

    assert isinstance(books, list)

    if books:
        first_book = books[0]
        assert first_book
        assert first_book.get("_id")
        assert first_book.get("title")
        assert first_book.get("author")
        assert first_book.get("description")
        assert first_book.get("genre")
        assert first_book.get("image")


@pytest.mark.usefixtures("mongo_test_db")
def test_insert_and_get_and_delete_book_by_id(book_repository: BookRepository, dracula_book: dict[str, str]) -> None:
    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    book_id = book_repository.insert_book(book={
        "image": image,
        "title": title,
        "author": author,
        "description": description,
        "genre": genre
    })

    assert book_id
    assert isinstance(book_id, str)

    book_id = ObjectId(book_id)

    assert isinstance(book_id, ObjectId)

    book = book_repository.get_book_by_id(book_id=book_id)

    assert book
    assert ObjectId(book.get("_id")) == book_id
    assert book.get("title") == title
    assert book.get("image") == image
    assert book.get("author") == author
    assert book.get("description") == description
    assert book.get("genre") == genre

    book_repository.delete_book_by_id(book_id=book_id)

    book = book_repository.get_book_by_id(book_id=book_id)

    assert not book

@pytest.mark.usefixtures("mongo_test_db")
def test_get_books_by_genre(book_repository: BookRepository, dracula_book: dict[str, str]) -> None:
    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    book_id = book_repository.insert_book(book={
        "image": image,
        "title": title,
        "author": author,
        "description": description,
        "genre": genre
    })

    books = book_repository.get_books_by_genre(genre=genre)

    assert books
    assert {"_id": book_id, "image": image, "title": title, "author": author, "description": description, "genre": genre} in books

    book_id = ObjectId(book_id)

    book_repository.delete_book_by_id(book_id=book_id)


@pytest.mark.usefixtures("mongo_test_db")
def test_get_books_by_genre(book_repository: BookRepository, dracula_book: dict[str, str]) -> None:
    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    book_id = book_repository.insert_book(book={
        "image": image,
        "title": title,
        "author": author,
        "description": description,
        "genre": genre
    })

    genres = book_repository.get_genres()

    assert genres
    assert genre in genres

    book_id = ObjectId(book_id)

    book_repository.delete_book_by_id(book_id=book_id)

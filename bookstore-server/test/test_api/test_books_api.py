import pytest

from flask import Flask
from flask import Response

from test.conftest import prefix_books_bp


def test_alive_books(flask_client: Flask) -> None:
    response: Response = flask_client.get(f"{prefix_books_bp}/alive")
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    version_bp = result.get("version_bp")
    author = result.get("author")
    name_bp = result.get("name_bp")

    assert status_code == 200
    assert message == "I am Alive!"
    assert version_bp == "2.0.0"
    assert author == "Diego Libonati"
    assert name_bp == "Books"


@pytest.mark.usefixtures("mongo_test_db")
def test_add_book(flask_client: Flask, dracula_book: dict[str, str]):
    response: Response = flask_client.post(
        f"{prefix_books_bp}/add",
        json=dracula_book,
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    book = result.get("data")

    inserted_id = book.get("_id")

    assert status_code == 201
    assert inserted_id
    assert message == "The book was successfully added."
    assert book
    assert type(book) == dict
    assert book.get("_id") == inserted_id
    assert book.get("image") == dracula_book.get("image")
    assert book.get("title") == dracula_book.get("title")
    assert book.get("author") == dracula_book.get("author")
    assert book.get("description") == dracula_book.get("description")
    assert book.get("genre") == dracula_book.get("genre")


@pytest.mark.usefixtures("mongo_test_db")
def test_add_book_error(flask_client: Flask):
    wrong_book = {
        "author": "",
        "title": "",
        "description": "",
        "image": "",
        "genre": ""
    }

    response: Response = flask_client.post(
        f"{prefix_books_bp}/add",
        json=wrong_book,
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    book = result.get("data")
    fields = result.get("fields")

    assert status_code == 400
    assert message == "The requested book could not be added."
    assert not book
    assert fields == wrong_book


@pytest.mark.usefixtures("mongo_test_db")
def test_get_books(flask_client: Flask, inserted_book_id: str, dracula_book: dict[str, str]) -> None:
    book = None

    response: Response = flask_client.get(f"{prefix_books_bp}/")
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    books = result.get("data")
    
    for b in books:
        if b.get("_id") == inserted_book_id:
            book = b

    assert status_code == 200
    assert message == "Books were successfully obtained."
    assert type(books) == list

    assert book
    assert type(book) == dict
    assert book.get("_id") == inserted_book_id
    assert book.get("image") == dracula_book.get("image")
    assert book.get("title") == dracula_book.get("title")
    assert book.get("author") == dracula_book.get("author")
    assert book.get("description") == dracula_book.get("description")
    assert book.get("genre") == dracula_book.get("genre")


@pytest.mark.usefixtures("mongo_test_db")
def test_get_books_by_genre(flask_client: Flask, inserted_book_id: str, dracula_book: dict[str, str]) -> None:
    book = None

    response: Response = flask_client.get(f"{prefix_books_bp}/{dracula_book.get('genre')}")
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    books = result.get("data")
    
    for b in books:
        if b.get("_id") == inserted_book_id:
            book = b

    assert status_code == 200
    assert message == "Books were successfully obtained."
    assert type(books) == list
    
    assert book
    assert type(book) == dict
    assert book.get("_id") == inserted_book_id
    assert book.get("image") == dracula_book.get("image")
    assert book.get("title") == dracula_book.get("title")
    assert book.get("author") == dracula_book.get("author")
    assert book.get("description") == dracula_book.get("description")
    assert book.get("genre") == dracula_book.get("genre")


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_book(flask_client: Flask, inserted_book_id: str) -> None:
    response: Response = flask_client.delete(f"{prefix_books_bp}/delete/{inserted_book_id}")
    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 200
    assert message == f"{inserted_book_id} was deleted."


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_wrong_book(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{prefix_books_bp}/delete/asd")
    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 400
    assert type(message) == str


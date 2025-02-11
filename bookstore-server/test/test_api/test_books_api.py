import pytest

from flask import Flask
from flask import Response

from test.constants import BLUEPRINTS
from test.constants import BOOK_MOCK


def test_alive_books(flask_client: Flask) -> None:
    response: Response = flask_client.get(f"{BLUEPRINTS['books']}/alive")
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
def test_add_book(flask_client: Flask, dracula_book: dict[str, str]) -> None:
    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    response: Response = flask_client.post(
        f"{BLUEPRINTS['books']}/add",
        json=dracula_book,
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 201
    assert message == "The book was successfully added."
    assert data
    assert type(data) == dict
    assert data.get("_id")
    assert data.get("image") == image
    assert data.get("title") == title
    assert data.get("author") == author
    assert data.get("description") == description
    assert data.get("genre") == genre


@pytest.mark.usefixtures("mongo_test_db")
def test_add_book_error(flask_client: Flask) -> None:
    wrong_book = {
        "author": "",
        "title": "",
        "description": "",
        "image": "",
        "genre": ""
    }

    response: Response = flask_client.post(
        f"{BLUEPRINTS['books']}/add",
        json=wrong_book,
    )
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    book = result.get("data")

    assert status_code == 400
    assert message == "The requested book could not be added."
    assert not book


@pytest.mark.usefixtures("mongo_test_db")
def test_get_books(flask_client: Flask, dracula_book: dict[str, str]) -> None:
    book = None

    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    response: Response = flask_client.get(f"{BLUEPRINTS['books']}/")
    
    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")
    
    assert status_code == 200
    assert message == "Books were successfully obtained."
    assert data
    assert type(data) == list

    for book in data:
        if book.get("title") == title and book.get("author") == author:
            book = book

    assert book
    assert book.get("_id")
    assert book.get("title") == title
    assert book.get("author") == author
    assert book.get("description") == description
    assert book.get("genre") == genre
    assert book.get("image") == image


@pytest.mark.usefixtures("mongo_test_db")
def test_get_books_by_genre(flask_client: Flask, dracula_book: dict[str, str]) -> None:
    book = None

    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    response: Response = flask_client.get(f"{BLUEPRINTS['books']}/{dracula_book.get('genre')}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")
    
    assert status_code == 200
    assert message == "Books were successfully obtained."
    assert data
    assert type(data) == list
    
    for book in data:
        if book.get("title") == title and book.get("author") == author:
            book = book

    assert book
    assert book.get("_id")
    assert book.get("title") == title
    assert book.get("author") == author
    assert book.get("description") == description
    assert book.get("genre") == genre
    assert book.get("image") == image


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_book(flask_client: Flask, dracula_book: dict[str, str]) -> None:
    image = dracula_book.get("image")
    title = dracula_book.get("title")
    author = dracula_book.get("author")
    description = dracula_book.get("description")
    genre = dracula_book.get("genre")

    response: Response = flask_client.get(
        f"{BLUEPRINTS['books']}/",
    )

    result = response.json
    book_to_delete = [book for book in result.get("data") if book.get("title") == title and book.get("author") == author][0]

    assert book_to_delete

    id_to_delete = book_to_delete.get("_id")

    response: Response = flask_client.delete(f"{BLUEPRINTS['books']}/delete/{id_to_delete}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 200
    assert message == f"Book with id: {id_to_delete} was deleted."
    assert isinstance(data, dict)

    assert data.get("_id") == id_to_delete
    assert data.get("title") == title
    assert data.get("image") == image
    assert data.get("author") == author
    assert data.get("description") == description
    assert data.get("genre") == genre


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_book_with_not_found_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{BLUEPRINTS['books']}/delete/{BOOK_MOCK['not_found_flag_id']}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")
    data = result.get("data")

    assert status_code == 404
    assert message == f"No book found with id: {BOOK_MOCK['not_found_flag_id']}."
    assert isinstance(message, str)
    assert not data


@pytest.mark.usefixtures("mongo_test_db")
def test_delete_book_with_wrong_id(flask_client: Flask) -> None:
    response: Response = flask_client.delete(f"{BLUEPRINTS['books']}/delete/{BOOK_MOCK['wrong_flag_id']}")

    result = response.json
    status_code = response.status_code

    message = result.get("message")

    assert status_code == 400
    assert isinstance(message, str)
    assert "Error deleting book:" in message


from src.utils.utils import parse_books


def test_parse_books() -> None:
    books = [{
        "_id": 1,
        "title": "Dracula",
        "description": "asd asd asd",
        "image": "123.jpg",
        "author": "Tom 123",
        "genre": "Terror"
    },
    {
        "_id": 2,
        "title": "Dracula 2",
        "description": "asd asd asd 2",
        "image": "1234.jpg",
        "author": "Tom 123",
        "genre": "Terror"
    }]

    books_parsed = parse_books(books=books)

    assert type(books_parsed) == list

    for book in books_parsed:
        assert book
        assert type(book.get("_id")) == str
        assert book.get("_id")
        assert book.get("title")
        assert book.get("description")
        assert book.get("image")
        assert book.get("author")
        assert book.get("genre")



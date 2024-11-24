from src.models.Book import Book


def test_book_model(book_model: Book, book_test: dict[str, str]) -> None:
    _id = book_test.get("_id")
    image = book_test.get("image")
    title = book_test.get("title")
    author = book_test.get("author")
    description = book_test.get("description")
    genre = book_test.get("genre")

    assert book_model
    assert isinstance(book_model, Book)
    assert book_model.id == _id
    assert book_model.title == title
    assert book_model.image == image
    assert book_model.author == author
    assert book_model.description == description
    assert book_model.genre == genre


def test_book_to_dict(book_model: Book, book_test: dict[str, str]) -> None:
    _id = book_test.get("_id")
    image = book_test.get("image")
    title = book_test.get("title")
    author = book_test.get("author")
    description = book_test.get("description")
    genre = book_test.get("genre")

    book_dict = book_model.to_dict()

    assert isinstance(book_dict, dict)
    assert book_dict.get("_id") == _id
    assert book_dict.get("title") == title
    assert book_dict.get("image") == image
    assert book_dict.get("author") == author
    assert book_dict.get("description") == description
    assert book_dict.get("genre") == genre
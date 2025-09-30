import pytest
from pydantic import ValidationError

from src.models.book_model import BookModel


def test_create_bookmodel_success(dracula_book: dict[str, str]) -> None:
    book = BookModel(**dracula_book)
    assert book.title == dracula_book.get("title")
    assert book.author == dracula_book.get("author")
    assert book.model_dump() == dracula_book


@pytest.mark.parametrize(
    "missing_field", ["title", "image", "author", "description", "genre"]
)
def test_create_bookmodel_missing_fields(
    dracula_book: dict[str, str], missing_field: str
) -> None:
    data = dracula_book.copy()
    data.pop(missing_field)

    with pytest.raises(ValidationError) as exc:
        BookModel(**data)

    assert missing_field in str(exc.value)


def test_create_bookmodel_invalid_type(dracula_book: dict[str, str]) -> None:
    data = {
        "title": 123,
        "image": dracula_book.get("image"),
        "author": dracula_book.get("author"),
        "description": dracula_book.get("description"),
        "genre": dracula_book.get("genre"),
    }
    with pytest.raises(ValidationError) as exc:
        BookModel(**data)

    assert "title" in str(exc.value)
    assert "string_type" in str(exc.value) or "str type expected" in str(exc.value)

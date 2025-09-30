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


@pytest.mark.parametrize(
    "invalid_field,invalid_value",
    [
        ("title", 123),
        ("author", ""),
        ("description", "   "),
    ],
)
def test_create_bookmodel_invalid_values(
    dracula_book: dict[str, str], invalid_field: str, invalid_value: str
) -> None:
    data = dracula_book.copy()
    data[invalid_field] = invalid_value

    with pytest.raises(ValidationError) as exc:
        BookModel(**data)

    assert invalid_field in str(exc.value)

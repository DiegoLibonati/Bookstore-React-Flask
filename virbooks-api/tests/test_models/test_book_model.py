from typing import Any

import pytest
from pydantic import ValidationError

from src.models.book_model import BookModel

VALID_BOOK_DATA: dict[str, str] = {
    "title": "Clean Code",
    "image": "https://example.com/image.jpg",
    "author": "Robert Martin",
    "description": "A handbook of agile software craftsmanship",
    "genre": "Technology",
}


@pytest.mark.unit
class TestBookModel:
    def test_valid_book_creation(self) -> None:
        book: BookModel = BookModel(**VALID_BOOK_DATA)
        assert book.title == "Clean Code"
        assert book.author == "Robert Martin"
        assert book.genre == "Technology"

    def test_empty_title_raises_validation_error(self) -> None:
        data: dict[str, str] = {**VALID_BOOK_DATA, "title": ""}
        with pytest.raises(ValidationError):
            BookModel(**data)

    def test_whitespace_only_field_raises_validation_error(self) -> None:
        data: dict[str, str] = {**VALID_BOOK_DATA, "title": "   "}
        with pytest.raises(ValidationError):
            BookModel(**data)

    def test_missing_required_field_raises_validation_error(self) -> None:
        data: dict[str, str] = {
            "title": "Clean Code",
            "image": "https://example.com/image.jpg",
            "author": "Robert Martin",
        }
        with pytest.raises(ValidationError):
            BookModel(**data)

    def test_model_dump_returns_all_expected_fields(self) -> None:
        book: BookModel = BookModel(**VALID_BOOK_DATA)
        dumped: dict[str, Any] = book.model_dump()
        assert set(dumped.keys()) == {"title", "image", "author", "description", "genre"}

    def test_whitespace_is_stripped_from_all_fields(self) -> None:
        data: dict[str, str] = {
            "title": "  Clean Code  ",
            "image": "  https://example.com/image.jpg  ",
            "author": "  Robert Martin  ",
            "description": "  A handbook  ",
            "genre": "  Technology  ",
        }
        book: BookModel = BookModel(**data)
        assert book.title == "Clean Code"
        assert book.author == "Robert Martin"
        assert book.genre == "Technology"

    def test_none_field_raises_validation_error(self) -> None:
        data: dict[str, str | None] = {**VALID_BOOK_DATA, "title": None}
        with pytest.raises(ValidationError):
            BookModel(**data)

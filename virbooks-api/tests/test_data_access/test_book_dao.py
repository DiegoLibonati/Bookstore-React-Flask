from typing import Any

import pytest
from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.data_access.book_dao import BookDAO

SAMPLE_BOOK: dict[str, str] = {
    "title": "Clean Code",
    "image": "https://example.com/image.jpg",
    "author": "Robert Martin",
    "description": "A handbook of agile software craftsmanship",
    "genre": "Technology",
}


@pytest.mark.unit
class TestBookDAOParseBook:
    def test_parse_book_returns_none_for_none_input(self) -> None:
        result: dict[str, Any] | None = BookDAO.parse_book(None)
        assert result is None

    def test_parse_book_converts_object_id_to_string(self) -> None:
        obj_id: ObjectId = ObjectId()
        raw_book: dict[str, Any] = {"_id": obj_id, "title": "Test Book", "author": "Author"}
        parsed: dict[str, Any] = BookDAO.parse_book(raw_book)
        assert isinstance(parsed["_id"], str)
        assert parsed["_id"] == str(obj_id)

    def test_parse_book_preserves_other_fields(self) -> None:
        obj_id: ObjectId = ObjectId()
        raw_book: dict[str, Any] = {"_id": obj_id, "title": "Test", "genre": "Fiction"}
        parsed: dict[str, Any] = BookDAO.parse_book(raw_book)
        assert parsed["title"] == "Test"
        assert parsed["genre"] == "Fiction"


@pytest.mark.integration
class TestBookDAOInsertOne:
    def test_insert_one_returns_result_with_id(self, app: Flask, mongo_db: Database) -> None:
        result: InsertOneResult = BookDAO.insert_one(SAMPLE_BOOK.copy())
        assert result.inserted_id is not None

    def test_inserted_book_is_persisted_in_collection(self, app: Flask, mongo_db: Database) -> None:
        BookDAO.insert_one(SAMPLE_BOOK.copy())
        books: list[dict[str, Any]] = BookDAO.find()
        assert len(books) == 1
        assert books[0]["title"] == "Clean Code"


@pytest.mark.integration
class TestBookDAOFind:
    def test_find_returns_empty_list_when_collection_is_empty(self, app: Flask, mongo_db: Database) -> None:
        books: list[dict[str, Any]] = BookDAO.find()
        assert books == []

    def test_find_returns_all_inserted_books(self, app: Flask, mongo_db: Database) -> None:
        BookDAO.insert_one({"title": "Book One", "author": "A", "image": "i", "description": "d", "genre": "Fiction"})
        BookDAO.insert_one({"title": "Book Two", "author": "B", "image": "i", "description": "d", "genre": "Tech"})
        books: list[dict[str, Any]] = BookDAO.find()
        assert len(books) == 2

    def test_find_returns_books_with_string_id(self, app: Flask, mongo_db: Database) -> None:
        BookDAO.insert_one(SAMPLE_BOOK.copy())
        books: list[dict[str, Any]] = BookDAO.find()
        assert isinstance(books[0]["_id"], str)


@pytest.mark.integration
class TestBookDAOFindByGenre:
    def test_find_by_genre_returns_matching_books(self, app: Flask, mongo_db: Database) -> None:
        BookDAO.insert_one({**SAMPLE_BOOK, "title": "Tech Book", "genre": "Technology"})
        BookDAO.insert_one({**SAMPLE_BOOK, "title": "Fiction Book", "author": "Other", "genre": "Fiction"})
        books: list[dict[str, Any]] = BookDAO.find_by_genre("Technology")
        assert len(books) == 1
        assert books[0]["genre"] == "Technology"

    def test_find_by_genre_returns_empty_list_when_no_match(self, app: Flask, mongo_db: Database) -> None:
        books: list[dict[str, Any]] = BookDAO.find_by_genre("NonExistentGenre")
        assert books == []


@pytest.mark.integration
class TestBookDAOFindOneById:
    def test_find_one_by_id_returns_book_when_found(self, app: Flask, mongo_db: Database) -> None:
        result: InsertOneResult = BookDAO.insert_one(SAMPLE_BOOK.copy())
        book_id: str = str(result.inserted_id)
        book: dict[str, Any] | None = BookDAO.find_one_by_id(book_id)
        assert book is not None
        assert book["title"] == "Clean Code"

    def test_find_one_by_id_returns_none_when_not_found(self, app: Flask, mongo_db: Database) -> None:
        fake_id: str = str(ObjectId())
        book: dict[str, Any] | None = BookDAO.find_one_by_id(fake_id)
        assert book is None


@pytest.mark.integration
class TestBookDAOFindOneByTitleAndAuthor:
    def test_find_one_by_title_and_author_returns_book_when_found(self, app: Flask, mongo_db: Database) -> None:
        BookDAO.insert_one(SAMPLE_BOOK.copy())
        book: dict[str, Any] | None = BookDAO.find_one_by_title_and_author("Clean Code", "Robert Martin")
        assert book is not None
        assert book["title"] == "Clean Code"
        assert book["author"] == "Robert Martin"

    def test_find_one_by_title_and_author_returns_none_when_not_found(self, app: Flask, mongo_db: Database) -> None:
        book: dict[str, Any] | None = BookDAO.find_one_by_title_and_author("NonExistent", "Unknown")
        assert book is None


@pytest.mark.integration
class TestBookDAODeleteOneById:
    def test_delete_one_by_id_returns_deleted_count_of_one(self, app: Flask, mongo_db: Database) -> None:
        result: InsertOneResult = BookDAO.insert_one(SAMPLE_BOOK.copy())
        book_id: str = str(result.inserted_id)
        delete_result: DeleteResult = BookDAO.delete_one_by_id(book_id)
        assert delete_result.deleted_count == 1

    def test_delete_one_by_id_removes_book_from_collection(self, app: Flask, mongo_db: Database) -> None:
        result: InsertOneResult = BookDAO.insert_one(SAMPLE_BOOK.copy())
        book_id: str = str(result.inserted_id)
        BookDAO.delete_one_by_id(book_id)
        book: dict[str, Any] | None = BookDAO.find_one_by_id(book_id)
        assert book is None

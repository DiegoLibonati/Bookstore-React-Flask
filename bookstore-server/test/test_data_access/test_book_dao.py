from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.data_access.book_dao import BookDAO


class TestBookDAOInsert:
    def test_insert_one_creates_document(
        self, app: Flask, mongo_db: Database, sample_book: dict[str, str]
    ) -> None:
        mongo_db.books.delete_many({})

        result = BookDAO.insert_one(sample_book.copy())

        assert result.inserted_id is not None

        doc = mongo_db.books.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["title"] == sample_book["title"]

    def test_insert_one_returns_insert_result(
        self, app: Flask, mongo_db: Database, sample_book: dict[str, str]
    ) -> None:
        mongo_db.books.delete_many({})

        result = BookDAO.insert_one(sample_book.copy())

        assert isinstance(result, InsertOneResult)
        assert result.acknowledged is True

    def test_insert_multiple_documents(
        self, app: Flask, mongo_db: Database, sample_books: list[dict[str, str]]
    ) -> None:
        mongo_db.books.delete_many({})

        for book in sample_books:
            BookDAO.insert_one(book.copy())

        count = mongo_db.books.count_documents({})
        assert count == len(sample_books)


class TestBookDAOFind:
    def test_find_returns_empty_list_when_no_documents(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        result = BookDAO.find()

        assert result == []

    def test_find_returns_all_documents(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        result = BookDAO.find()

        assert len(result) == len(inserted_books)

    def test_find_returns_parsed_documents(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        result = BookDAO.find()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestBookDAOFindByGenre:
    def test_find_by_genre_returns_matching_documents(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        result = BookDAO.find_by_genre("Test")

        assert len(result) == len(inserted_books)

    def test_find_by_genre_returns_empty_for_nonexistent_genre(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        result = BookDAO.find_by_genre("NonExistentGenre")

        assert result == []

    def test_find_by_genre_returns_parsed_documents(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        result = BookDAO.find_by_genre("Test")

        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_find_by_genre_is_case_sensitive(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        result_lowercase = BookDAO.find_by_genre("test")
        result_uppercase = BookDAO.find_by_genre("TEST")

        assert result_lowercase == []
        assert result_uppercase == []


class TestBookDAOFindOneById:
    def test_find_one_by_id_returns_document(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        book_id = inserted_books[0]["_id"]

        result = BookDAO.find_one_by_id(book_id)

        assert result is not None
        assert result["_id"] == book_id
        assert result["title"] == inserted_books[0]["title"]

    def test_find_one_by_id_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})
        fake_id = str(ObjectId())

        result = BookDAO.find_one_by_id(fake_id)

        assert result is None

    def test_find_one_by_id_accepts_string_id(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        book_id = inserted_books[0]["_id"]

        result = BookDAO.find_one_by_id(book_id)

        assert result is not None
        assert isinstance(result["_id"], str)


class TestBookDAOFindOneByTitleAndAuthor:
    def test_find_one_by_title_and_author_returns_document(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        book = inserted_books[0]

        result = BookDAO.find_one_by_title_and_author(book["title"], book["author"])

        assert result is not None
        assert result["title"] == book["title"]
        assert result["author"] == book["author"]

    def test_find_one_by_title_and_author_returns_none_for_nonexistent(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        result = BookDAO.find_one_by_title_and_author(
            "Nonexistent Title", "Nonexistent Author"
        )

        assert result is None

    def test_find_one_by_title_and_author_requires_both_match(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        book = inserted_books[0]

        result = BookDAO.find_one_by_title_and_author(book["title"], "Wrong Author")
        assert result is None

        result = BookDAO.find_one_by_title_and_author("Wrong Title", book["author"])
        assert result is None


class TestBookDAODelete:
    def test_delete_one_by_id_removes_document(
        self, app: Flask, inserted_books: list[dict[str, str]], mongo_db: Database
    ) -> None:
        book_id = inserted_books[0]["_id"]
        initial_count = mongo_db.books.count_documents({})

        result = BookDAO.delete_one_by_id(book_id)

        assert result.deleted_count == 1
        assert mongo_db.books.count_documents({}) == initial_count - 1

    def test_delete_one_by_id_returns_delete_result(
        self, app: Flask, inserted_books: list[dict[str, str]]
    ) -> None:
        book_id = inserted_books[0]["_id"]

        result = BookDAO.delete_one_by_id(book_id)

        assert isinstance(result, DeleteResult)
        assert result.acknowledged is True

    def test_delete_one_by_id_nonexistent_returns_zero(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})
        fake_id = str(ObjectId())

        result = BookDAO.delete_one_by_id(fake_id)

        assert result.deleted_count == 0

    def test_delete_one_by_id_only_removes_one(
        self, app: Flask, inserted_books: list[dict[str, str]], mongo_db: Database
    ) -> None:
        book_id = inserted_books[0]["_id"]
        initial_count = mongo_db.books.count_documents({})

        BookDAO.delete_one_by_id(book_id)

        final_count = mongo_db.books.count_documents({})
        assert final_count == initial_count - 1


class TestBookDAOParsing:
    def test_parse_book_converts_id_to_string(self, app: Flask) -> None:
        doc = {"_id": ObjectId(), "title": "Test", "author": "Author"}

        result = BookDAO.parse_book(doc)

        assert isinstance(result["_id"], str)

    def test_parse_book_preserves_other_fields(self, app: Flask) -> None:
        doc = {
            "_id": ObjectId(),
            "title": "Test Title",
            "author": "Test Author",
            "genre": "Test Genre",
            "extra_field": "extra_value",
        }

        result = BookDAO.parse_book(doc)

        assert result["title"] == "Test Title"
        assert result["author"] == "Test Author"
        assert result["genre"] == "Test Genre"
        assert result["extra_field"] == "extra_value"

    def test_parse_book_returns_none_for_none(self, app: Flask) -> None:
        result = BookDAO.parse_book(None)

        assert result is None

    def test_parse_books_handles_list(self, app: Flask) -> None:
        docs = [
            {"_id": ObjectId(), "title": "Book 1", "author": "Author 1"},
            {"_id": ObjectId(), "title": "Book 2", "author": "Author 2"},
        ]

        result = BookDAO.parse_books(docs)

        assert len(result) == 2
        assert all(isinstance(doc["_id"], str) for doc in result)

    def test_parse_books_handles_empty_list(self, app: Flask) -> None:
        result = BookDAO.parse_books([])

        assert result == []

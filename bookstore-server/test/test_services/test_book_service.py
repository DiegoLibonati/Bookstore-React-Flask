import pytest
from bson import ObjectId
from flask import Flask
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import CODE_ERROR_BOOK_ALREADY_EXISTS, CODE_NOT_FOUND_BOOK
from src.models.book_model import BookModel
from src.services.book_service import BookService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestBookServiceAddBook:
    def test_add_book_inserts_document(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.books.delete_many({})

        book = BookModel(
            title="New Book",
            image="new.jpg",
            author="New Author",
            description="New Description",
            genre="New Genre",
        )

        result = BookService.add_book(book)

        assert result.inserted_id is not None

        doc = mongo_db.books.find_one({"_id": result.inserted_id})
        assert doc is not None
        assert doc["title"] == "New Book"

    def test_add_book_returns_insert_result(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        book = BookModel(
            title="Another Book",
            image="another.jpg",
            author="Another Author",
            description="Another Description",
            genre="Another Genre",
        )

        result = BookService.add_book(book)

        assert isinstance(result, InsertOneResult)

    def test_add_book_raises_conflict_for_duplicate(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        book = BookModel(
            title="Duplicate Book",
            image="dup.jpg",
            author="Duplicate Author",
            description="Description",
            genre="Genre",
        )

        BookService.add_book(book)

        with pytest.raises(ConflictAPIError) as exc_info:
            BookService.add_book(book)

        assert exc_info.value.status_code == 409
        assert exc_info.value.code == CODE_ERROR_BOOK_ALREADY_EXISTS

    def test_add_book_allows_same_title_different_author(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        book1 = BookModel(
            title="Same Title",
            image="img1.jpg",
            author="Author One",
            description="Description 1",
            genre="Genre",
        )

        book2 = BookModel(
            title="Same Title",
            image="img2.jpg",
            author="Author Two",
            description="Description 2",
            genre="Genre",
        )

        BookService.add_book(book1)
        result = BookService.add_book(book2)

        assert result.inserted_id is not None

    def test_add_book_allows_same_author_different_title(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        book1 = BookModel(
            title="Title One",
            image="img1.jpg",
            author="Same Author",
            description="Description 1",
            genre="Genre",
        )

        book2 = BookModel(
            title="Title Two",
            image="img2.jpg",
            author="Same Author",
            description="Description 2",
            genre="Genre",
        )

        BookService.add_book(book1)
        result = BookService.add_book(book2)

        assert result.inserted_id is not None


class TestBookServiceGetAllBooks:
    def test_get_all_books_returns_empty_list(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        result = BookService.get_all_books()

        assert result == []

    def test_get_all_books_returns_all(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result = BookService.get_all_books()

        assert len(result) == len(inserted_templates)

    def test_get_all_books_returns_parsed_documents(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result = BookService.get_all_books()

        assert len(result) > 0
        assert all(isinstance(doc["_id"], str) for doc in result)


class TestBookServiceGetAllBooksByGenre:
    def test_get_all_books_by_genre_returns_matching(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result = BookService.get_all_books_by_genre("Test")

        assert len(result) == len(inserted_templates)

    def test_get_all_books_by_genre_returns_empty_for_nonexistent(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result = BookService.get_all_books_by_genre("NonExistentGenre")

        assert result == []

    def test_get_all_books_by_genre_is_case_sensitive(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result_lowercase = BookService.get_all_books_by_genre("test")
        result_uppercase = BookService.get_all_books_by_genre("TEST")

        assert result_lowercase == []
        assert result_uppercase == []


class TestBookServiceGetAllGenres:
    def test_get_all_genres_returns_empty_list(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        result = BookService.get_all_genres()

        assert result == []

    def test_get_all_genres_returns_unique_genres(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result = BookService.get_all_genres()

        assert "Test" in result
        assert len(result) == 1

    def test_get_all_genres_returns_list(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        result = BookService.get_all_genres()

        assert isinstance(result, list)

    def test_get_all_genres_with_multiple_genres(
        self, app: Flask, mongo_db: Database
    ) -> None:
        mongo_db.books.delete_many({})

        mongo_db.books.insert_many(
            [
                {
                    "title": "Book 1",
                    "image": "img1.jpg",
                    "author": "Author 1",
                    "description": "Desc 1",
                    "genre": "Horror",
                },
                {
                    "title": "Book 2",
                    "image": "img2.jpg",
                    "author": "Author 2",
                    "description": "Desc 2",
                    "genre": "Romance",
                },
                {
                    "title": "Book 3",
                    "image": "img3.jpg",
                    "author": "Author 3",
                    "description": "Desc 3",
                    "genre": "Horror",
                },
                {
                    "title": "Book 4",
                    "image": "img4.jpg",
                    "author": "Author 4",
                    "description": "Desc 4",
                    "genre": "Sci-Fi",
                },
            ]
        )

        result = BookService.get_all_genres()

        assert len(result) == 3
        assert set(result) == {"Horror", "Romance", "Sci-Fi"}


class TestBookServiceDeleteBookById:
    def test_delete_book_removes_document(
        self, app: Flask, inserted_templates: list[dict[str, str]], mongo_db: Database
    ) -> None:
        book_id = inserted_templates[0]["_id"]
        initial_count = mongo_db.books.count_documents({})

        BookService.delete_book_by_id(book_id)

        final_count = mongo_db.books.count_documents({})
        assert final_count == initial_count - 1

    def test_delete_book_returns_delete_result(
        self, app: Flask, inserted_templates: list[dict[str, str]]
    ) -> None:
        book_id = inserted_templates[0]["_id"]

        result = BookService.delete_book_by_id(book_id)

        assert isinstance(result, DeleteResult)

    def test_delete_book_raises_not_found(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.books.delete_many({})
        fake_id = str(ObjectId())

        with pytest.raises(NotFoundAPIError) as exc_info:
            BookService.delete_book_by_id(fake_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.code == CODE_NOT_FOUND_BOOK

    def test_delete_book_only_removes_one(
        self, app: Flask, inserted_templates: list[dict[str, str]], mongo_db: Database
    ) -> None:
        book_id = inserted_templates[0]["_id"]
        initial_count = mongo_db.books.count_documents({})

        BookService.delete_book_by_id(book_id)

        final_count = mongo_db.books.count_documents({})
        assert final_count == initial_count - 1


class TestBookServiceIntegration:
    def test_full_crud_cycle(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.books.delete_many({})

        book = BookModel(
            title="CRUD Book",
            image="crud.jpg",
            author="CRUD Author",
            description="CRUD Description",
            genre="CRUD Genre",
        )

        create_result = BookService.add_book(book)
        book_id = str(create_result.inserted_id)

        books = BookService.get_all_books()
        assert len(books) == 1
        assert books[0]["_id"] == book_id

        delete_result = BookService.delete_book_by_id(book_id)
        assert delete_result.deleted_count == 1

        books = BookService.get_all_books()
        assert len(books) == 0

    def test_multiple_books_management(self, app: Flask, mongo_db: Database) -> None:
        mongo_db.books.delete_many({})

        books_data = [
            {
                "title": "Book A",
                "image": "a.jpg",
                "author": "Author A",
                "description": "Desc A",
                "genre": "Genre A",
            },
            {
                "title": "Book B",
                "image": "b.jpg",
                "author": "Author B",
                "description": "Desc B",
                "genre": "Genre B",
            },
            {
                "title": "Book C",
                "image": "c.jpg",
                "author": "Author C",
                "description": "Desc C",
                "genre": "Genre A",
            },
        ]

        ids = []
        for data in books_data:
            result = BookService.add_book(BookModel(**data))
            ids.append(str(result.inserted_id))

        books = BookService.get_all_books()
        assert len(books) == 3

        genres = BookService.get_all_genres()
        assert len(genres) == 2

        BookService.delete_book_by_id(ids[1])

        books = BookService.get_all_books()
        assert len(books) == 2
        assert all(b["title"] != "Book B" for b in books)

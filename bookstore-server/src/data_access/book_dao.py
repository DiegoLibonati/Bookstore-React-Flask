from typing import Any

from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from config.mongo_config import mongo


class BookDAO:
    @staticmethod
    def insert_one(book: dict) -> InsertOneResult:
        return mongo.db.books.insert_one(book)

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return BookDAO.parse_books(list(mongo.db.books.find()))

    @staticmethod
    def find_by_genre(genre: str) -> list[dict[str, Any]]:
        return BookDAO.parse_books(list(mongo.db.books.find({"genre": genre})))

    @staticmethod
    def find_by_id(_id: ObjectId) -> dict[str, Any] | None:
        return mongo.db.books.find_one({"_id": ObjectId(_id)})

    @staticmethod
    def find_one_by_title_and_author(title: str, author: str) -> dict[str, Any] | None:
        return mongo.db.books.find_one({"title": title, "author": author})

    def delete_one_by_id(_id: ObjectId) -> DeleteResult:
        return mongo.db.books.delete_one({"_id": ObjectId(_id)})

    @staticmethod
    def parse_books(books: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {**{k: v for k, v in book.items() if k != "_id"}, "_id": str(book["_id"])}
            for book in books
        ]

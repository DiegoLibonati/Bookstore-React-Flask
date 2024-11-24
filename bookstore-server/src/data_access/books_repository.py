from typing import Any
from bson import ObjectId

from flask_pymongo.wrappers import Database


class BookRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def get_all_books(self) -> list[dict[str, Any]]:
        return list(self.db.books.find())
    
    def get_book_by_id(self, book_id: ObjectId) -> list[dict[str, Any]]:
        return self.db.books.find_one({"_id": book_id})

    def get_books_by_genre(self, genre: str) -> list[dict[str, Any]]:
        return list(self.db.books.find({
            "genre": genre
        }))
    
    def get_genres(self) -> list[str]:
        return list(self.db.books.distinct("genre"))
    
    def insert_book(self, book: dict[str, Any]) -> str:
        result = self.db.books.insert_one(book)
        return str(result.inserted_id)
    
    def delete_book_by_id(self, book_id: ObjectId) -> bool:
        result = self.db.books.delete_one({"_id": book_id})
        return bool(result.deleted_count)
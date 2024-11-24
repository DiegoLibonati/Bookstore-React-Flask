from typing import Any

from src.models.Book import Book
from src.models.Manager import Manager


class BookManager(Manager[Book]):
    def __init__(self) -> None:
        super().__init__(items={}, initializer=Book)

    @property
    def books(self) -> list[Book]:
        return self.items_values
    
    def add_book(self, book: Book) -> None:
        if not book or not isinstance(book, Book): raise TypeError("You must enter a valid book in order to add it.")

        super()._add_item(item=book)

    def add_books(self, books: list[dict[str, Any]]) -> None:
        if not isinstance(books, list): raise TypeError("You must enter a valid books to add its.")

        super()._add_items(items=books)

    def __str__(self) -> str:
        return f"\n----- BOOKMANAGER START -----\n" \
        f"Books: {self.parse_items()}\n" \
        f"----- BOOKMANAGER END -----\n"
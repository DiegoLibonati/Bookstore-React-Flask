from typing import Any

def parse_books(books: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**book, "_id": str(book["_id"])} for book in books]
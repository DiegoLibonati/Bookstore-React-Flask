import pytest

from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_BOOK,
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_INTERNAL_SERVER,
    MESSAGE_ERROR_PYDANTIC,
    MESSAGE_NOT_FOUND_BOOK,
    MESSAGE_SUCCESS_ADD_BOOK,
    MESSAGE_SUCCESS_DELETE_BOOK,
    MESSAGE_SUCCESS_GET_ALL_BOOKS,
    MESSAGE_SUCCESS_GET_ALL_GENRES,
)


@pytest.mark.unit
class TestSuccessMessages:
    def test_message_success_add_book_value(self) -> None:
        assert MESSAGE_SUCCESS_ADD_BOOK == "The book was successfully added."

    def test_message_success_get_all_books_value(self) -> None:
        assert MESSAGE_SUCCESS_GET_ALL_BOOKS == "Books were successfully obtained."

    def test_message_success_get_all_genres_value(self) -> None:
        assert MESSAGE_SUCCESS_GET_ALL_GENRES == "The book genres were successfully obtained."

    def test_message_success_delete_book_value(self) -> None:
        assert MESSAGE_SUCCESS_DELETE_BOOK == "Book was successfully deleted."


@pytest.mark.unit
class TestErrorMessages:
    def test_message_error_internal_server_value(self) -> None:
        assert MESSAGE_ERROR_INTERNAL_SERVER == "Internal server error."

    def test_message_error_pydantic_value(self) -> None:
        assert MESSAGE_ERROR_PYDANTIC == "Pydantic error."

    def test_message_error_database_value(self) -> None:
        assert MESSAGE_ERROR_DATABASE == "Database error."

    def test_message_error_generic_contains_placeholder(self) -> None:
        assert "{e}" in MESSAGE_ERROR_GENERIC


@pytest.mark.unit
class TestConflictAndNotFoundMessages:
    def test_message_already_exists_book_value(self) -> None:
        assert MESSAGE_ALREADY_EXISTS_BOOK == "Book already exists."

    def test_message_not_found_book_value(self) -> None:
        assert MESSAGE_NOT_FOUND_BOOK == "No book found."


@pytest.mark.unit
class TestMessagesUniqueness:
    def test_all_messages_are_unique(self) -> None:
        all_messages: list[str] = [
            MESSAGE_SUCCESS_ADD_BOOK,
            MESSAGE_SUCCESS_GET_ALL_BOOKS,
            MESSAGE_SUCCESS_GET_ALL_GENRES,
            MESSAGE_SUCCESS_DELETE_BOOK,
            MESSAGE_ERROR_INTERNAL_SERVER,
            MESSAGE_ERROR_PYDANTIC,
            MESSAGE_ERROR_DATABASE,
            MESSAGE_ERROR_GENERIC,
            MESSAGE_ALREADY_EXISTS_BOOK,
            MESSAGE_NOT_FOUND_BOOK,
        ]
        assert len(all_messages) == len(set(all_messages))

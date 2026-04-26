import pytest

from src.constants.codes import (
    CODE_ALREADY_EXISTS_BOOK,
    CODE_ERROR_DATABASE,
    CODE_ERROR_GENERIC,
    CODE_ERROR_INTERNAL_SERVER,
    CODE_ERROR_PYDANTIC,
    CODE_NOT_FOUND_BOOK,
    CODE_SUCCESS_ADD_BOOK,
    CODE_SUCCESS_DELETE_BOOK,
    CODE_SUCCESS_GET_ALL_BOOKS,
    CODE_SUCCESS_GET_ALL_GENRES,
)


@pytest.mark.unit
class TestSuccessCodes:
    def test_code_success_add_book_value(self) -> None:
        assert CODE_SUCCESS_ADD_BOOK == "SUCCESS_ADD_BOOK"

    def test_code_success_get_all_books_value(self) -> None:
        assert CODE_SUCCESS_GET_ALL_BOOKS == "SUCCESS_GET_ALL_BOOKS"

    def test_code_success_get_all_genres_value(self) -> None:
        assert CODE_SUCCESS_GET_ALL_GENRES == "SUCCESS_GET_ALL_GENRES"

    def test_code_success_delete_book_value(self) -> None:
        assert CODE_SUCCESS_DELETE_BOOK == "SUCCESS_DELETE_BOOK"


@pytest.mark.unit
class TestErrorCodes:
    def test_code_error_internal_server_value(self) -> None:
        assert CODE_ERROR_INTERNAL_SERVER == "ERROR_INTERNAL_SERVER"

    def test_code_error_pydantic_value(self) -> None:
        assert CODE_ERROR_PYDANTIC == "ERROR_PYDANTIC"

    def test_code_error_database_value(self) -> None:
        assert CODE_ERROR_DATABASE == "ERROR_DATABASE"

    def test_code_error_generic_value(self) -> None:
        assert CODE_ERROR_GENERIC == "ERROR_GENERIC"


@pytest.mark.unit
class TestConflictAndNotFoundCodes:
    def test_code_already_exists_book_value(self) -> None:
        assert CODE_ALREADY_EXISTS_BOOK == "ALREADY_EXISTS_BOOK"

    def test_code_not_found_book_value(self) -> None:
        assert CODE_NOT_FOUND_BOOK == "NOT_FOUND_BOOK"


@pytest.mark.unit
class TestCodesUniqueness:
    def test_all_codes_are_unique(self) -> None:
        all_codes: list[str] = [
            CODE_SUCCESS_ADD_BOOK,
            CODE_SUCCESS_GET_ALL_BOOKS,
            CODE_SUCCESS_GET_ALL_GENRES,
            CODE_SUCCESS_DELETE_BOOK,
            CODE_ERROR_INTERNAL_SERVER,
            CODE_ERROR_PYDANTIC,
            CODE_ERROR_DATABASE,
            CODE_ERROR_GENERIC,
            CODE_ALREADY_EXISTS_BOOK,
            CODE_NOT_FOUND_BOOK,
        ]
        assert len(all_codes) == len(set(all_codes))

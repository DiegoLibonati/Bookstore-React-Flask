from typing import Any

import pytest
from pydantic import BaseModel, ValidationError
from pymongo.errors import PyMongoError

from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_INTERNAL_SERVER, CODE_ERROR_PYDANTIC
from src.utils.exceptions import (
    BaseAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)
from src.utils.exceptions_decorator import exceptions_decorator


class SampleModel(BaseModel):
    value: int


@pytest.mark.unit
class TestExceptionsDecoratorPassthrough:
    def test_returns_value_when_no_exception_raised(self) -> None:
        @exceptions_decorator
        def fn() -> str:
            return "ok"

        result: str = fn()

        assert result == "ok"

    def test_preserves_dict_return_value(self) -> None:
        expected: dict[str, Any] = {"key": "value", "count": 1}

        @exceptions_decorator
        def fn() -> dict[str, Any]:
            return expected

        result: dict[str, Any] = fn()

        assert result == expected

    def test_preserves_args_and_kwargs(self) -> None:
        @exceptions_decorator
        def fn(a: int, b: int, c: int = 0) -> int:
            return a + b + c

        result: int = fn(1, 2, c=3)

        assert result == 6

    def test_preserves_function_name_via_functools_wraps(self) -> None:
        @exceptions_decorator
        def my_custom_handler() -> None:
            return None

        assert my_custom_handler.__name__ == "my_custom_handler"


@pytest.mark.unit
class TestExceptionsDecoratorDomainErrors:
    def test_propagates_base_api_error_unchanged(self) -> None:
        original: BaseAPIError = BaseAPIError(code="X", message="Y", status_code=418)

        @exceptions_decorator
        def fn() -> None:
            raise original

        with pytest.raises(BaseAPIError) as exc_info:
            fn()

        assert exc_info.value is original

    def test_propagates_not_found_api_error_unchanged(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise NotFoundAPIError(code="NF", message="missing")

        with pytest.raises(NotFoundAPIError) as exc_info:
            fn()

        assert exc_info.value.status_code == 404

    def test_propagates_conflict_api_error_unchanged(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise ConflictAPIError(code="C", message="conflict")

        with pytest.raises(ConflictAPIError) as exc_info:
            fn()

        assert exc_info.value.status_code == 409


@pytest.mark.unit
class TestExceptionsDecoratorPydanticErrors:
    def test_raises_validation_api_error_on_pydantic_validation_error(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            SampleModel(value="not-an-int")

        with pytest.raises(ValidationAPIError):
            fn()

    def test_validation_api_error_has_status_400(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            SampleModel(value="not-an-int")

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()

        assert exc_info.value.status_code == 400

    def test_validation_api_error_has_pydantic_code(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            SampleModel(value="not-an-int")

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()

        assert exc_info.value.code == CODE_ERROR_PYDANTIC

    def test_validation_api_error_contains_details_in_payload(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            SampleModel(value="not-an-int")

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()

        assert "details" in exc_info.value.payload
        assert isinstance(exc_info.value.payload["details"], list)


@pytest.mark.unit
class TestExceptionsDecoratorMongoErrors:
    def test_raises_internal_api_error_on_pymongo_error(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise PyMongoError("connection refused")

        with pytest.raises(InternalAPIError):
            fn()

    def test_internal_api_error_has_status_500(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise PyMongoError("timeout")

        with pytest.raises(InternalAPIError) as exc_info:
            fn()

        assert exc_info.value.status_code == 500

    def test_internal_api_error_has_database_code(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise PyMongoError("oops")

        with pytest.raises(InternalAPIError) as exc_info:
            fn()

        assert exc_info.value.code == CODE_ERROR_DATABASE

    def test_pymongo_error_is_chained_as_cause(self) -> None:
        original: PyMongoError = PyMongoError("boom")

        @exceptions_decorator
        def fn() -> None:
            raise original

        with pytest.raises(InternalAPIError) as exc_info:
            fn()

        assert exc_info.value.__cause__ is original


@pytest.mark.unit
class TestExceptionsDecoratorUnexpectedErrors:
    def test_raises_internal_api_error_on_unexpected_exception(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise RuntimeError("unexpected")

        with pytest.raises(InternalAPIError):
            fn()

    def test_internal_api_error_has_internal_server_code(self) -> None:
        @exceptions_decorator
        def fn() -> None:
            raise RuntimeError("unexpected")

        with pytest.raises(InternalAPIError) as exc_info:
            fn()

        assert exc_info.value.code == CODE_ERROR_INTERNAL_SERVER

    def test_unexpected_exception_is_chained_as_cause(self) -> None:
        original: ValueError = ValueError("nope")

        @exceptions_decorator
        def fn() -> None:
            raise original

        with pytest.raises(InternalAPIError) as exc_info:
            fn()

        assert exc_info.value.__cause__ is original

    def test_validation_error_caught_only_when_raised_from_pydantic(self) -> None:
        with pytest.raises(ValidationError):
            SampleModel(value="not-an-int")

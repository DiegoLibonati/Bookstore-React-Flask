from typing import Any

import pytest
from pydantic import BaseModel, ValidationError
from pymongo.errors import PyMongoError

from src.utils.exceptions import InternalAPIError, ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


class SampleModel(BaseModel):
    value: int


@pytest.mark.unit
class TestExceptionsHandler:
    def test_returns_value_when_no_exception_raised(self) -> None:
        @exceptions_handler
        def fn() -> str:
            return "ok"

        result: str = fn()
        assert result == "ok"

    def test_preserves_dict_return_value(self) -> None:
        expected: dict[str, Any] = {"key": "value", "count": 1}

        @exceptions_handler
        def fn() -> dict[str, Any]:
            return expected

        result: dict[str, Any] = fn()
        assert result == expected

    def test_raises_internal_api_error_on_pymongo_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise PyMongoError("connection refused")

        with pytest.raises(InternalAPIError):
            fn()

    def test_internal_api_error_has_status_500(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise PyMongoError("timeout")

        with pytest.raises(InternalAPIError) as exc_info:
            fn()

        assert exc_info.value.status_code == 500

    def test_raises_validation_api_error_on_pydantic_validation_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            try:
                SampleModel(value="not-an-int")
            except ValidationError:
                raise

        with pytest.raises(ValidationAPIError):
            fn()

    def test_validation_api_error_contains_details_in_payload(self) -> None:
        @exceptions_handler
        def fn() -> None:
            try:
                SampleModel(value="not-an-int")
            except ValidationError:
                raise

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()

        error: ValidationAPIError = exc_info.value
        assert error.status_code == 400
        assert "details" in error.payload

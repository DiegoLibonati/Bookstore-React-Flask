import pytest

from src.constants.codes import CODE_ERROR_API
from src.constants.messages import MESSAGE_ERROR_API
from src.utils.exceptions import (
    BaseAPIError,
    ConflictAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


def test_base_api_error_defaults() -> None:
    err: BaseAPIError = BaseAPIError()
    assert err.status_code == 500
    assert err.message == MESSAGE_ERROR_API
    assert err.code == CODE_ERROR_API
    assert err.payload == {}
    assert err.to_dict() == {
        "code": CODE_ERROR_API,
        "message": MESSAGE_ERROR_API,
        "payload": {},
    }


def test_base_api_error_custom_values() -> None:
    err: BaseAPIError = BaseAPIError(
        code="CUSTOM_CODE",
        message="Custom message",
        status_code=418,
        payload={"extra": "data"},
    )
    assert err.status_code == 418
    assert err.message == "Custom message"
    assert err.code == "CUSTOM_CODE"
    assert err.payload == {"extra": "data"}
    assert err.to_dict() == {
        "code": "CUSTOM_CODE",
        "message": "Custom message",
        "payload": {"extra": "data"},
    }


@pytest.mark.parametrize(
    "error_cls,expected_status,expected_message",
    [
        (ValidationAPIError, 400, "Validation error"),
        (NotFoundAPIError, 404, "Resource not found"),
        (ConflictAPIError, 409, "Conflict error"),
    ],
)
def test_specific_api_errors(
    error_cls: type[BaseAPIError], expected_status: int, expected_message: str
) -> None:
    err: BaseAPIError = error_cls()
    assert err.status_code == expected_status
    assert err.message == expected_message
    assert err.code == CODE_ERROR_API
    assert err.to_dict()["message"] == expected_message

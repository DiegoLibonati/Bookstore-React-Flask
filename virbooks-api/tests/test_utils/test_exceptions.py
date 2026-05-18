from typing import Any

import pytest
from flask import Flask

from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    BusinessAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


@pytest.fixture()
def flask_app_context() -> Any:
    app: Flask = Flask(__name__)
    with app.app_context():
        yield


@pytest.mark.unit
class TestBaseAPIError:
    def test_default_status_code_is_500(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.status_code == 500

    def test_custom_status_code_is_set(self) -> None:
        error: BaseAPIError = BaseAPIError(status_code=418)
        assert error.status_code == 418

    def test_custom_message_is_set(self) -> None:
        error: BaseAPIError = BaseAPIError(message="custom error")
        assert error.message == "custom error"

    def test_to_dict_contains_code_and_message(self) -> None:
        error: BaseAPIError = BaseAPIError(code="TEST_CODE", message="test message")
        result: dict[str, Any] = error.to_dict()
        assert result["code"] == "TEST_CODE"
        assert result["message"] == "test message"

    def test_to_dict_excludes_payload_key_when_empty(self) -> None:
        error: BaseAPIError = BaseAPIError()
        result: dict[str, Any] = error.to_dict()
        assert "payload" not in result

    def test_to_dict_includes_payload_when_provided(self) -> None:
        error: BaseAPIError = BaseAPIError(code="TEST", message="msg", payload={"key": "value"})
        result: dict[str, Any] = error.to_dict()
        assert result["payload"] == {"key": "value"}

    def test_is_exception_subclass(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestExceptionSubclasses:
    def test_validation_api_error_has_status_400(self) -> None:
        error: ValidationAPIError = ValidationAPIError()
        assert error.status_code == 400

    def test_authentication_api_error_has_status_401(self) -> None:
        error: AuthenticationAPIError = AuthenticationAPIError()
        assert error.status_code == 401

    def test_not_found_api_error_has_status_404(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError()
        assert error.status_code == 404

    def test_conflict_api_error_has_status_409(self) -> None:
        error: ConflictAPIError = ConflictAPIError()
        assert error.status_code == 409

    def test_business_api_error_has_status_422(self) -> None:
        error: BusinessAPIError = BusinessAPIError()
        assert error.status_code == 422

    def test_internal_api_error_has_status_500(self) -> None:
        error: InternalAPIError = InternalAPIError()
        assert error.status_code == 500

    def test_all_subclasses_are_base_api_error_instances(self) -> None:
        subclass_errors: list[BaseAPIError] = [
            ValidationAPIError(),
            AuthenticationAPIError(),
            NotFoundAPIError(),
            ConflictAPIError(),
            BusinessAPIError(),
            InternalAPIError(),
        ]
        for error in subclass_errors:
            assert isinstance(error, BaseAPIError)

    def test_custom_message_overrides_subclass_default(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError(message="Book not found")
        assert error.message == "Book not found"

    def test_custom_code_overrides_subclass_default(self) -> None:
        error: ConflictAPIError = ConflictAPIError(code="CUSTOM_CODE")
        assert error.code == "CUSTOM_CODE"


@pytest.mark.unit
class TestBaseAPIErrorFlaskResponse:
    def test_flask_response_returns_status_code(self, flask_app_context: None) -> None:
        error: BaseAPIError = BaseAPIError(code="X", message="msg", status_code=418)

        _, status_code = error.flask_response()

        assert status_code == 418

    def test_flask_response_body_contains_code_and_message(self, flask_app_context: None) -> None:
        error: ConflictAPIError = ConflictAPIError(code="C", message="conflict")

        response, _ = error.flask_response()
        data: dict[str, Any] = response.get_json()

        assert data["code"] == "C"
        assert data["message"] == "conflict"

    def test_flask_response_body_includes_payload_when_present(self, flask_app_context: None) -> None:
        error: ValidationAPIError = ValidationAPIError(
            code="V",
            message="invalid",
            payload={"details": [{"field": "title"}]},
        )

        response, _ = error.flask_response()
        data: dict[str, Any] = response.get_json()

        assert data["payload"] == {"details": [{"field": "title"}]}

    def test_flask_response_omits_payload_when_empty(self, flask_app_context: None) -> None:
        error: BaseAPIError = BaseAPIError(code="X", message="msg")

        response, _ = error.flask_response()
        data: dict[str, Any] = response.get_json()

        assert "payload" not in data

    def test_flask_response_uses_subclass_default_status(self, flask_app_context: None) -> None:
        error: NotFoundAPIError = NotFoundAPIError(code="NF", message="missing")

        _, status_code = error.flask_response()

        assert status_code == 404

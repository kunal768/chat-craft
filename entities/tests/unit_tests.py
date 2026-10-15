# python -m pytest tests/unit_tests.py -v
import pytest
from datetime import datetime
from src.app.core.utils.errors import (
    CustomException,
    UserNotFoundError,
    InvalidCredentialsError,
    EmailAlreadyExistsError,
)
from src.app.core.utils.status_codes import StatusCodes
from src.app.core.utils.error_handler import ErrorHandler
from src.app.schemas.std_response import StdResponse
from src.app.models.user import User
from src.app.models.update_interval import UpdateInterval
from src.app.models.doctype import DocType

# Test Custom Exceptions
def test_custom_exception():
    exception = CustomException("Test error", 400)
    assert exception.message == "Test error"
    assert exception.status_code == 400

def test_user_not_found_error():
    error = UserNotFoundError()
    assert error.message == "User not found"
    assert error.status_code == StatusCodes.NOT_FOUND

def test_invalid_credentials_error():
    error = InvalidCredentialsError()
    assert error.message == "Invalid credentials"
    assert error.status_code == StatusCodes.UNAUTHORIZED

def test_email_already_exists_error():
    error = EmailAlreadyExistsError()
    assert error.message == "Email already exists"
    assert error.status_code == StatusCodes.BAD_REQUEST

# Test Error Handler
def test_error_handler_custom_exception():
    error = UserNotFoundError()
    response = ErrorHandler.handle_error(error)
    assert isinstance(response, StdResponse)
    assert response.success is False
    assert response.status_code == StatusCodes.NOT_FOUND.value
    assert response.error == "User not found"

def test_error_handler_unexpected_error():
    error = Exception("Unexpected error")
    response = ErrorHandler.handle_error(error)
    assert isinstance(response, StdResponse)
    assert response.success is False
    assert response.status_code == StatusCodes.INTERNAL_SERVER_ERROR.value
    assert response.error == "Unexpected error"

def test_error_handler_success():
    data = {"test": "data"}
    response = ErrorHandler.handle_success(data, "Test success")
    assert isinstance(response, StdResponse)
    assert response.success is True
    assert response.status_code == StatusCodes.SUCCESS.value
    assert response.data == data
    assert response.message == "Test success"

# Test User Model
def test_user_model():
    user = User(
        email="test@example.com",
        name="Test User"
    )
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)

def test_user_model_validation():
    with pytest.raises(ValueError):
        User(
            email="invalid-email",
            name="Test User"
        )

# Test Update Interval Enum
def test_update_interval():
    assert UpdateInterval.TIME_NONE.value == -1
    assert UpdateInterval.TIME_FIVE.value == 5
    assert UpdateInterval.TIME_THIRTY.value == 30
    assert UpdateInterval.TIME_HOUR.value == 60
    assert UpdateInterval.TIME_DAY.value == 1440

# Test DocType Enum
def test_doctype():
    assert DocType.PDF.name == "PDF"
    assert DocType.DOCX.name == "DOCX"
    assert DocType.GOOGLE_SHEET.name == "GOOGLE_SHEET"
    assert DocType.GOOGLE_DOC.name == "GOOGLE_DOC"
    assert DocType.CSV.name == "CSV"

import pydantic
import pytest

from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.currency_code import (
    CurrencyCode,
)


def test_currency_code_constructor() -> None:
    # Arrange
    expected = "USD"

    # Act
    result = CurrencyCode(value=expected)

    # Assert
    assert result.value == expected


def test_imutability() -> None:
    # Arrange
    code = CurrencyCode(value="EUR")

    # Act / Assert
    with pytest.raises(pydantic.ValidationError, match="frozen"):
        code.value = "new"


def test_create_fn_returns_result() -> None:
    # Arrange
    expected = "USD"

    # Act
    result = CurrencyCode.create(value=expected)

    # Assert
    assert isinstance(result, Result)


def test_create_fn_default_value() -> None:
    # Arrange
    expected = "EUR"

    # Act
    result = CurrencyCode.create()

    # Assert
    assert result.is_success()
    assert result.unwrap() == CurrencyCode(value=expected)


def test_create_fn_success() -> None:
    # Arrange
    expected = "USD"

    # Act
    result = CurrencyCode.create(value=expected)

    # Assert
    assert result.is_success()
    assert result.unwrap() == CurrencyCode(value=expected)


def test_create_invalid_currency_code() -> None:
    result = CurrencyCode.create("To_long")

    assert result.is_failure()
    with pytest.raises(pydantic.ValidationError):
        result.unwrap()
    result = CurrencyCode.create("sh")

    assert result.is_failure()
    with pytest.raises(pydantic.ValidationError):
        result.unwrap()
    result = CurrencyCode.create(53)

    assert result.is_failure()
    with pytest.raises(pydantic.ValidationError):
        result.unwrap()

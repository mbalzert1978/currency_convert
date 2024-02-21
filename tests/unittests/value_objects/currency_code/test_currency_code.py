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


def test_create_fn_default_value() -> None:
    # Arrange
    expected = "EUR"

    # Act
    result = CurrencyCode.create().unwrap()

    # Assert
    assert result == CurrencyCode(value=expected)


def test_create_fn_success() -> None:
    # Arrange
    expected = "USD"

    # Act
    result = CurrencyCode.create(value=expected).unwrap()

    # Assert
    assert result == CurrencyCode(value=expected)


def test_create_invalid_currency_code() -> None:
    with pytest.raises(pydantic.ValidationError):
        CurrencyCode.create("To_long").unwrap()

    with pytest.raises(pydantic.ValidationError):
        CurrencyCode.create("sh").unwrap()

    with pytest.raises(pydantic.ValidationError):
        CurrencyCode.create(53).unwrap()

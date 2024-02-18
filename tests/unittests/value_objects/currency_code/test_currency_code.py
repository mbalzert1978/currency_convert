import pydantic
import pytest

from currency_convert.core.domain.shared.value_objects.currency_code import (
    CurrencyCode,
)


def test_create_valid_currency_code() -> None:
    # Arrange
    expected = "USD"

    # Act
    constructor = CurrencyCode(value=expected)
    create_fn = CurrencyCode.create(expected)

    # Assert
    assert constructor.value == expected
    assert isinstance(create_fn, CurrencyCode)
    assert create_fn.value == expected


def test_create_invalid_currency_code() -> None:
    with pytest.raises(pydantic.ValidationError):
        CurrencyCode.create("To_long")

    with pytest.raises(pydantic.ValidationError):
        CurrencyCode.create("sh")

    with pytest.raises(pydantic.ValidationError):
        CurrencyCode.create(53)


def test_imutability() -> None:
    # Arrange
    code = CurrencyCode.create()

    # Act / Assert
    with pytest.raises(pydantic.ValidationError, match="frozen"):
        code.value = "new"

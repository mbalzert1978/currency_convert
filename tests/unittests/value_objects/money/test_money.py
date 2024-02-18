import decimal

import pydantic
import pytest

from currency_convert.core.domain.shared.value_objects.money import (
    PRECISION,
    Money,
)


def test_create_valid_money() -> None:
    # Arrange
    value = "123.45"
    expected = decimal.Decimal(value).quantize(PRECISION)

    # Act
    money = Money.create(value)

    # Assert
    assert isinstance(money, Money)
    assert money.value == expected


def test_create_invalid_money() -> None:
    with pytest.raises(pydantic.ValidationError):
        Money.create("bad")

    with pytest.raises(pydantic.ValidationError):
        Money.create(list)


def test_imutability() -> None:
    # Arrange
    money = Money.create()

    # Act / Assert
    with pytest.raises(pydantic.ValidationError, match="frozen"):
        money.value = "new"

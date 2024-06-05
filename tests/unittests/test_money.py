import decimal
from typing import Any

import pytest

from currency_convert.domain.agency.valueobjects.money import (
    FormatError,
    Money,
    NegativeError,
)


# Creational, Equality, and Get Values Tests
@pytest.mark.parametrize(
    "input_str, expected, comparison, expected_result, expected_values",
    [
        (
            "100",
            decimal.Decimal("100.00000000"),
            "100.00000000",
            True,
            [decimal.Decimal("100.00000000")],
        ),
        (
            "100",
            decimal.Decimal("100.00000000"),
            "200.00000000",
            False,
            [decimal.Decimal("100.00000000")],
        ),
        (
            " 100 ",
            decimal.Decimal("100.00000000"),
            "100.00000000",
            True,
            [decimal.Decimal("100.00000000")],
        ),
    ],
    ids=[
        "Money_from_str_when_valid_value_should_return_money_instance_and_equality_should_return_true",
        "Money_from_str_when_valid_value_should_return_money_instance_and_equality_should_return_false",
        "Money_from_str_when_whitespace_should_return_money_instance_and_equality_should_return_true",
    ],
)
def test_Money_from_str_when_valid_value_should_return_expected_results(
    input_str: str,
    expected: Any,
    comparison: str,
    expected_result: bool,
    expected_values: list[decimal.Decimal],
) -> None:
    money = Money.from_str(input_str)
    assert money.amount == expected
    assert (money == Money.from_str(comparison)) == expected_result
    values = list(money.get_values())
    assert values == expected_values


# Error Tests
@pytest.mark.parametrize(
    "input_str, exception",
    [
        ("-100", NegativeError),
        ("0", NegativeError),
        ("invalid", FormatError),
        ("", FormatError),
        ("100.abc", FormatError),
        ("1.2.3", FormatError),
        ("100,00", FormatError),
    ],
    ids=[
        "Money_from_str_when_negative_value_should_raise_negative_error",
        "Money_from_str_when_zero_value_should_raise_negative_error",
        "Money_from_str_when_invalid_format_should_raise_format_error",
        "Money_from_str_when_empty_string_should_raise_format_error",
        "Money_from_str_when_non_numeric_characters_should_raise_format_error",
        "Money_from_str_when_multiple_decimal_points_should_raise_format_error",
        "Money_from_str_when_comma_instead_of_dot_should_raise_format_error",
    ],
)
def test_Money_from_str_when_invalid_value_should_raise_expected_errors(
    input_str: str, exception: type[Exception]
) -> None:
    with pytest.raises(exception):
        Money.from_str(input_str)

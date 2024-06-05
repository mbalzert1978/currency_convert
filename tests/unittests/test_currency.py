import pytest

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.primitives.valueobject import ValueObjectError


# Creational and Equality Tests
@pytest.mark.parametrize(
    "code, expected_code, comparison, expected_result, expected_values",
    [
        ("USD", "USD", "USD", True, ["USD"]),
        ("USD", "USD", "EUR", False, ["USD"]),
    ],
    ids=[
        "create_when_code_is_valid_length_should_return_currency_instance_and_equality_should_return_true",
        "create_when_code_is_valid_length_should_return_currency_instance_and_equality_should_return_false",
    ],
)
def test_create_and_equality_when_code_is_valid_length_should_return_expected_results(
    code: str,
    expected_code: str,
    comparison: str,
    expected_result: bool,
    expected_values: list[str],
) -> None:
    currency = Currency.from_str(code)
    assert currency.code == expected_code
    assert (currency == comparison) == expected_result
    values = list(currency.get_values())
    assert values == expected_values


# Error Tests
@pytest.mark.parametrize(
    "code",
    [
        ("US"),
        ("U"),
        ("USDE"),
        ("123"),
        (""),
    ],
    ids=[
        "create_when_code_is_invalid_length_should_raise_value_object_error",
        "create_when_code_is_too_short_should_raise_value_object_error",
        "create_when_code_is_too_long_should_raise_value_object_error",
        "create_when_code_is_numeric_should_raise_value_object_error",
        "create_when_code_is_empty_should_raise_value_object_error",
    ],
)
def test_create_when_code_is_invalid_length_should_raise_value_object_error(
    code: str,
) -> None:
    with pytest.raises(ValueObjectError):
        Currency.from_str(code)

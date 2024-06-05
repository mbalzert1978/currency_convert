import datetime

import pytest

from currency_convert.domain.agency.valueobjects.currency import (
    Currency,
    InvalidCurrencyError,
)
from currency_convert.domain.agency.valueobjects.money import (
    FormatError,
    Money,
    NegativeError,
)
from currency_convert.domain.agency.valueobjects.rate import InvalidDateError, Rate


# Creational, Equality, and Get Values Tests
@pytest.mark.parametrize(
    "currency_from, currency_to, rate, date, expected_currency_from, expected_currency_to, expected_rate, expected_date",
    [
        (
            "USD",
            "EUR",
            "0.85",
            "2023-10-01T00:00:00",
            Currency(code="USD"),
            Currency(code="EUR"),
            Money.from_str("0.85"),
            datetime.datetime(2023, 10, 1, 0, 0, 0),
        ),
        (
            "USD",
            "EUR",
            "1.23456789",
            "2023-10-01T00:00:00",
            Currency(code="USD"),
            Currency(code="EUR"),
            Money.from_str("1.23456789"),  # No rounding for 8 decimal places
            datetime.datetime(2023, 10, 1, 0, 0, 0),
        ),
        (
            "USD",
            "EUR",
            "1.234567880",
            "2023-10-01T00:00:00",
            Currency(code="USD"),
            Currency(code="EUR"),
            Money.from_str("1.23456788"),  # Rounding for 9 decimal places round down
            datetime.datetime(2023, 10, 1, 0, 0, 0),
        ),
        (
            "USD",
            "EUR",
            "1.234567886",
            "2023-10-01T00:00:00",
            Currency(code="USD"),
            Currency(code="EUR"),
            Money.from_str("1.23456789"),  # Rounding for 9 decimal places round up
            datetime.datetime(2023, 10, 1, 0, 0, 0),
        ),
    ],
    ids=[
        "Rate_create_when_all_parameters_are_valid_should_return_rate_instance",
        "Rate_create_when_rate_has_eight_decimal_places_should_not_round",
        "Rate_create_when_rate_has_nine_decimal_places_should_round__down_and_return_rate_instance",
        "Rate_create_when_rate_has_nine_decimal_places_should_round_up_and_return_rate_instance",
    ],
)
def test_create_when_all_parameters_are_valid_should_return_rate_instance(
    currency_from: str,
    currency_to: str,
    rate: str,
    date: str,
    expected_currency_from: Currency,
    expected_currency_to: Currency,
    expected_rate: Money,
    expected_date: datetime.datetime,
) -> None:
    rate_instance = Rate.create(
        currency_from, currency_to, rate, datetime.datetime.fromisoformat(date)
    )
    assert rate_instance.currency_from == expected_currency_from
    assert rate_instance.currency_to == expected_currency_to
    assert rate_instance.rate == expected_rate
    assert rate_instance.dt == expected_date


# Error Tests
@pytest.mark.parametrize(
    "currency_from, currency_to, rate, date, expected_error",
    [
        (
            "US",
            "EUR",
            "0.85",
            datetime.datetime(2023, 10, 1, 0, 0, 0),
            InvalidCurrencyError,
        ),
        (
            "USD",
            "EUR",
            "invalid_rate",
            datetime.datetime(2023, 10, 1, 0, 0, 0),
            FormatError,
        ),
        (
            "USD",
            "EUR",
            "0.85",
            "invalid_date",
            InvalidDateError,
        ),  # This test uses a string for date
        ("USD", "EUR", "0.00", datetime.datetime(2023, 10, 1, 0, 0, 0), NegativeError),
        ("USD", "EUR", "-0.85", datetime.datetime(2023, 10, 1, 0, 0, 0), NegativeError),
        (
            "USDE",
            "EUR",
            "0.85",
            datetime.datetime(2023, 10, 1, 0, 0, 0),
            InvalidCurrencyError,
        ),
        ("USD", "EUR", "0.85", "", InvalidDateError),
    ],
    ids=[
        "Rate_create_when_currency_code_is_invalid_should_return_invalid_currency_error",
        "Rate_create_when_rate_format_is_invalid_should_return_format_error",
        "Rate_create_when_date_format_is_invalid_should_return_value_error",
        "Rate_create_when_rate_is_zero_should_return_negative_error",
        "Rate_create_when_rate_is_negative_should_return_negative_error",
        "Rate_create_when_currency_code_is_too_long_should_return_invalid_currency_error",
        "Rate_create_when_date_is_empty_should_return_value_error",
    ],
)
def test_create_when_invalid_parameters_should_return_expected_errors(
    currency_from: str,
    currency_to: str,
    rate: str,
    date: str | datetime.datetime,
    expected_error: type[Exception],
) -> None:
    with pytest.raises(expected_error):
        Rate.create(currency_from, currency_to, rate, date)  # type: ignore[arg-type]

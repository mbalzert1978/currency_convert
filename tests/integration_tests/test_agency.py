import uuid
from datetime import datetime
from typing import Any

import pytest

from currency_convert.domain.agency.entities.agency import Agency, RateNotFoundError
from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import Money
from currency_convert.domain.agency.valueobjects.rate import Rate


@pytest.fixture
def agency() -> Agency:
    return Agency.create("USD", "Test Agency", "https://test.com", "Test Country")


@pytest.mark.parametrize(
    "base, name, address, country, expected_base, expected_name, expected_address, expected_country",
    [
        (
            "USD",
            "Test Agency",
            "https://test.com",
            "Test Country",
            "USD",
            "Test Agency",
            "https://test.com",
            "Test Country",
        ),
    ],
    ids=[
        "Agency_create_when_valid_attributes_should_return_agency_instance",
    ],
)
def test_create_when_valid_attributes_should_return_agency_instance(
    base: str,
    name: str,
    address: str,
    country: str,
    expected_base: str,
    expected_name: str,
    expected_address: str,
    expected_country: str,
) -> None:
    agency = Agency.create(base, name, address, country)
    assert agency.base == Currency.from_str(expected_base)
    assert agency.name == expected_name
    assert agency.address == expected_address
    assert agency.country == expected_country


@pytest.mark.parametrize(
    "id, base, name, address, country, rates, expected_base, expected_name, expected_address, expected_country",
    [
        (
            str(uuid.uuid4()),
            "USD",
            "Test Agency",
            "https://test.com",
            "Test Country",
            set(),
            "USD",
            "Test Agency",
            "https://test.com",
            "Test Country",
        ),
    ],
    ids=[
        "Agency_from_attributes_when_valid_attributes_should_return_agency_instance",
    ],
)
def test_from_attributes_when_valid_attributes_should_return_agency_instance(
    id: str,
    base: str,
    name: str,
    address: str,
    country: str,
    rates: set[Rate],
    expected_base: str,
    expected_name: str,
    expected_address: str,
    expected_country: str,
) -> None:
    agency = Agency.from_attributes(id, base, name, address, country, rates)
    assert agency.base == Currency.from_str(expected_base)
    assert agency.name == expected_name
    assert agency.address == expected_address
    assert agency.country == expected_country


@pytest.mark.parametrize(
    "currency_from, currency_to, date, expected_error",
    [
        (
            "USD",
            "EUR",
            datetime.fromisoformat("2023-10-01T00:00:00"),
            RateNotFoundError,
        ),
    ],
    ids=[
        "get_rate_when_rate_not_found_should_raise_rate_not_found_error",
    ],
)
def test_get_rate_when_rate_not_found_should_raise_rate_not_found_error(
    agency: Agency,
    currency_from: str,
    currency_to: str,
    date: datetime,
    expected_error: Any,
) -> None:
    with pytest.raises(expected_error):
        agency.get_rate(currency_from, currency_to, date)


@pytest.mark.parametrize(
    "rate1, rate2, expected_rate1, expected_rate2",
    [
        (
            ("USD", "EUR", "0.85", "2023-10-01T00:00:00"),
            ("USD", "EUR", "0.86", "2023-10-02T00:00:00"),
            Money.from_str("0.86"),
            Money.from_str("0.85"),
        ),
        (
            ("USD", "EUR", "0.90", "2023-10-03T00:00:00"),
            ("USD", "EUR", "0.80", "2023-10-01T00:00:00"),
            Money.from_str("0.90"),
            Money.from_str("0.80"),
        ),
    ],
    ids=[
        "get_rates_when_multiple_rates_should_return_sorted_rates_case_1",
        "get_rates_when_multiple_rates_should_return_sorted_rates_case_2",
    ],
)
def test_get_rates_when_multiple_rates_should_return_sorted_rates(
    agency: Agency,
    rate1: tuple[Any, ...],
    rate2: tuple[Any, ...],
    expected_rate1: Money,
    expected_rate2: Money,
) -> None:
    agency.add_rate(*rate1)
    agency.add_rate(*rate2)
    rates = agency.get_rates()
    assert len(rates) == 2
    assert rates[0].rate == expected_rate1
    assert rates[1].rate == expected_rate2


def test_get_rate_when_no_base_should_calculate_rate(agency: Agency) -> None:
    agency.add_rate("USD", "GBP", "0.75", "2023-10-01T00:00:00")
    agency.add_rate("USD", "EUR", "1.20", "2023-10-01T00:00:00")
    rate = agency.get_rate("GBP", "EUR")
    expected_rate = Money.from_str("1.60")  # 1 / 0.75 * 1.20
    assert rate.rate == expected_rate


def test_get_rate_when_base_should_return_rate(agency: Agency) -> None:
    agency.add_rate("USD", "JPY", "110.00", "2023-10-01T00:00:00")
    agency.add_rate("JPY", "EUR", "0.0075", "2023-10-01T00:00:00")
    rate = agency.get_rate("USD", "JPY")
    expected_rate = Money.from_str("110.00")
    assert rate.rate == expected_rate


def test_get_rate_when_to_is_base_should_return_inverted_rate(agency: Agency) -> None:
    agency.add_rate("USD", "CAD", "1.25", "2023-10-01T00:00:00")
    agency.add_rate("USD", "EUR", "0.65", "2023-10-01T00:00:00")
    rate = agency.get_rate("EUR", "USD")
    expected_rate = Money.from_str("1.53846154")  # 1 / 0.65
    assert rate.rate == expected_rate


def test_get_rate_when_base_and_no_date_should_return_latest_rate(
    agency: Agency,
) -> None:
    agency.add_rate("USD", "JPY", "110.00", "2023-10-01T00:00:00")
    agency.add_rate("USD", "JPY", "115.00", "2023-09-01T00:00:00")
    agency.add_rate("USD", "JPY", "120.00", "2023-08-01T00:00:00")
    rate = agency.get_rate("USD", "JPY")
    expected_rate = Money.from_str("110.00")
    assert rate.rate == expected_rate


def test_get_rate_when_base_and_date_should_return_rate_from_date(
    agency: Agency,
) -> None:
    agency.add_rate("USD", "JPY", "110.00", "2023-10-01T00:00:00")
    agency.add_rate("USD", "JPY", "115.00", "2023-09-01T00:00:00")
    agency.add_rate("USD", "JPY", "120.00", "2023-08-01T00:00:00")
    rate = agency.get_rate("USD", "JPY", datetime.fromisoformat("2023-08-01T00:00:00"))
    expected_rate = Money.from_str("120.00")
    assert rate.rate == expected_rate

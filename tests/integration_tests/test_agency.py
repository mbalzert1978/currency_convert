import uuid

import pytest
from results import Some

from currency_convert.domain.agency.entities.agency import (
    Agency,
    RateNotFoundError,
)
from currency_convert.domain.agency.entities.interface import UnprocessedRate
from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import Money
from currency_convert.domain.agency.valueobjects.rate import Rate


@pytest.fixture
def agency() -> Agency:
    return Agency(
        address="https://test.com",
        id=uuid.uuid4(),
        base=Currency.create("USD").unwrap(),
        name="Test Agency",
        country="Test Country",
    )


def test_add_rate(agency: Agency) -> None:
    result = agency.add_rate(
        currency_from="USD", currency_to="EUR", rate="0.85", date="2023-10-01"
    )
    assert result.is_ok()
    assert len(agency.rates) == 1


def test_add_rates(agency: Agency) -> None:
    rates = [
        UnprocessedRate(
            currency_from="USD",
            currency_to="EUR",
            rate="0.85",
            date="2023-10-01",
        ),
        UnprocessedRate(
            currency_from="USD",
            currency_to="GBP",
            rate="0.75",
            date="2023-10-01",
        ),
    ]
    result = agency.update(lambda: rates)
    assert result.is_ok()
    assert len(agency.rates) == 2


def test_get_rate(agency: Agency) -> None:
    agency.add_rate("USD", "EUR", "0.85", "2023-10-01")
    agency.add_rate("USD", "EUR", "0.95", "2023-10-02")
    result = agency.get_rate("USD", "EUR", "2023-10-01")
    assert result.is_ok()
    assert result.unwrap().rate == Money.create("0.85").unwrap()
    result = agency.get_rate("EUR", "USD", "2023-10-01")
    assert result.is_ok()
    assert result.unwrap().rate == Money.create("1.17647059").unwrap()
    result = agency.get_rate("USD", "JPY", "2023-10-01")
    assert result.is_err()
    assert isinstance(result.unwrap_err(), RateNotFoundError)


def test_list_rates(agency: Agency) -> None:
    agency.add_rate("USD", "EUR", "0.85", "2023-10-01")
    agency.add_rate("USD", "GBP", "0.75", "2023-10-01")
    result = agency.get_rates()
    assert result.is_ok()
    assert len(res := result.unwrap()) == 2
    assert Some(
        Rate.create(
            currency_from="USD",
            currency_to="EUR",
            rate="0.85",
            iso_str="2023-10-01",
        )
    ), (
        Some(
            Rate.create(
                currency_from="USD",
                currency_to="GBP",
                rate="0.75",
                iso_str="2023-10-01",
            )
        )
        == res
    )


def test_add_unprocessable_rates(agency: Agency) -> None:
    rates = [
        UnprocessedRate(
            currency_from="INVALID",
            currency_to="EUR",
            rate="0.85",
            date="2023-10-01",
        ),
        UnprocessedRate(
            currency_from="USD",
            currency_to="INVALID",
            rate="0.75",
            date="2023-10-01",
        ),
    ]
    result = agency.update(lambda: rates)
    assert result.is_err()
    assert len(agency.rates) == 0


def test_get_rate_no_base_currency(agency: Agency) -> None:
    # Add rates that do not include the base currency
    agency.add_rate("USD", "EUR", "0.85", "2023-10-01")
    agency.add_rate("USD", "JPY", "150.00", "2023-10-01")
    agency.add_rate("USD", "GBP", "0.75", "2023-10-01")

    # Attempt to get a rate that requires the base currency
    result = agency.get_rate("EUR", "JPY", "2023-10-01")
    assert result.is_ok()
    assert (
        result.unwrap()
        == Rate.create(
            currency_from="EUR",
            currency_to="JPY",
            rate="176.47058850",
            iso_str="2023-10-01",
        ).unwrap()
    )


def test_get_rate_with_date_range(agency: Agency) -> None:
    # Add rates for different dates
    agency.add_rate("USD", "EUR", "0.85", "2023-10-01")
    agency.add_rate("USD", "EUR", "0.86", "2023-09-30")
    agency.add_rate("USD", "EUR", "0.87", "2023-09-29")

    # Attempt to get a rate for a date range
    result = agency.get_rate("USD", "EUR", "2023-09-29", "2023-10-01")
    assert result.is_ok()
    assert result.unwrap().rate == Money.create("0.87").unwrap()

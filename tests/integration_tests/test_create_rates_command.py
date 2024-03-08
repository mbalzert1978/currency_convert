import random
from decimal import Decimal

from currency_convert.core.app.rate.create.rate.command import CreateRates
from currency_convert.core.app.rate.create.rate.handler import CreateRatesHandler
from currency_convert.core.app.rate.create.rates.command import CreateRate
from currency_convert.core.app.rate.create.rates.handler import CreateRateHandler
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money
from tests.helper.fake_repository import FakeRepository

CURRENCIES = (
    "USD",
    "JPY",
    "HRK",
    "PHP",
    "ADJ",
    "BOA",
    "TET",
)


def test_rates_can_be_created_from_command_handler() -> None:
    # Arrange
    agency = Agency.create(
        "test",
        CurrencyCode.create(),
        Country.create(),
    )
    rates = [
        Rate.create(
            agency.id_,
            CurrencyCode.create(CURRENCIES[v]),
            Money.create(Decimal(v)),
        )
        for v in range(1, 6)
    ]

    cmd = CreateRates(
        agency_name=agency.name,
        rates=rates,
    )
    handler = CreateRatesHandler(
        FakeRepository[Agency]({agency}), FakeRepository[Rate]()
    )

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_success()


def test_not_found_agency() -> None:
    # Arrange
    cmd = CreateRate(
        agency_name="test",
        to_currency=CurrencyCode.create("USD"),
        rate=Money.create(Decimal(random.expovariate(1))),
    )
    handler = CreateRateHandler(FakeRepository[Agency](), FakeRepository[Rate]())

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_failure()


def test_error_on_agency_search() -> None:
    # Arrange
    cmd = CreateRate(
        agency_name="test",
        to_currency=CurrencyCode.create("USD"),
        rate=Money.create(Decimal(random.expovariate(1))),
    )
    handler = CreateRateHandler(
        FakeRepository[Agency](raise_on="find_by_name", exc=Error(500, "Test_error")),
        FakeRepository[Rate](),
    )

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_failure()
    assert isinstance(result.failure(), Error)


def test_error_on_adding_rate() -> None:
    # Arrange
    agency = Agency.create(
        "test",
        CurrencyCode.create(),
        Country.create(),
    )
    cmd = CreateRate(
        agency_name=agency.name,
        to_currency=CurrencyCode.create("USD"),
        rate=Money.create(Decimal(random.expovariate(1))),
    )
    handler = CreateRateHandler(
        FakeRepository[Agency]({agency}),
        FakeRepository[Rate](raise_on="add", exc=Error(500, "Test_error")),
    )

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_failure()
    assert isinstance(result.failure(), Error)

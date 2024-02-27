from decimal import Decimal
import random
import pytest
from currency_convert.core.app.agency.create.command import CreateAgency
from currency_convert.core.app.agency.create.handler import CreateAgencyHandler
from currency_convert.core.app.rate.create.many.command import CreateRates
from currency_convert.core.app.rate.create.many.handler import CreateRatesHandler
from currency_convert.core.app.rate.create.single.command import CreateRate
from currency_convert.core.app.rate.create.single.handler import CreateRateHandler
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money
from tests.helper.fake_repository import FakeRepository


@pytest.fixture()
def insert_agency() -> FakeRepository[Agency]:
    repo = FakeRepository[Agency]()
    CreateAgencyHandler(repo).handle(
        CreateAgency(
            name="test_agency",
            base_currency=CurrencyCode.create(),
            residing_country=Country.create(),
        )
    )
    return repo


def test_rates_can_be_created_from_command_handler(
    insert_agency: FakeRepository[Agency],
) -> None:
    # Arrange
    currency_codes = ("USD", "JPY", "HRK", "PHP", "ADJ", "BOA", "TET")
    agency = insert_agency._get_first_entity()
    if agency is None:
        pytest.fail("No agency in test_repo.")

    cmd = CreateRates(
        agency_name="test_agency",
        rates=[
            Rate.create(
                agency.id_,
                CurrencyCode.create(random.choice(currency_codes)),
                Money.create(Decimal(random.expovariate(1))),
            )
            for _ in range(5)
        ],
    )
    r_repo = FakeRepository[Rate]()
    handler = CreateRatesHandler(insert_agency, r_repo)

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_success()


def test_result_is_handled_correct_on_exception(
    insert_agency: FakeRepository[Agency],
) -> None:
    agency = insert_agency._get_first_entity()
    if agency is None:
        pytest.fail("No agency in test_repo.")

    cmd = CreateRate(
        agency_name="test_agency",
        base_currency=CurrencyCode.create(),
        to_currency=CurrencyCode.create("USD"),
        rate=Money.create(Decimal(random.expovariate(1))),
        residing_coutry=Country.create(),
    )
    r_repo = FakeRepository[Rate](raise_on="add")
    handler = CreateRateHandler(insert_agency, r_repo)

    # Act
    res = handler.handle(cmd)

    assert res

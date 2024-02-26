from decimal import Decimal
import pytest
from currency_convert.core.app.agency.create.command import CreateAgency
from currency_convert.core.app.agency.create.handler import CreateAgencyHandler
from currency_convert.core.app.rate.create.single.command import CreateRate
from currency_convert.core.app.rate.create.single.handler import CreateRateHandler
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money
from tests.helper.fake_repository import FakeRepository


@pytest.fixture()
def insert_agency():
    CreateAgencyHandler(FakeRepository[Agency]()).handle(
        CreateAgency(
            name="test_agency",
            base_currency=CurrencyCode.create(),
            residing_country=Country.create(),
        )
    )


@pytest.mark.usefixtures("insert_agency")
def test_rate_can_be_created_from_command_handler() -> None:
    # Arrange
    cmd = CreateRate(
        agency_name="test_agency",
        base_currency=CurrencyCode.create(),
        to_currency=CurrencyCode.create("USD"),
        rate=Money.create(Decimal("1.25")),
        residing_coutry=Country.create(),
    )
    a_repo = FakeRepository[Agency]()
    r_repo = FakeRepository[Rate]()
    handler = CreateRateHandler(a_repo, r_repo)

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_success()

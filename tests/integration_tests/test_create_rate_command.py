from decimal import Decimal
from currency_convert.core.app.rate.create.single.command import CreateRate
from currency_convert.core.app.rate.create.single.handler import CreateRateHandler
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money
from tests.helper.fake_repository import FakeRepository


def test_rate_can_be_created_from_command_handler() -> None:
    # Arrange
    agency = Agency.create(
        "test",
        base_currency=CurrencyCode.create(),
        residing_country=Country.create(),
    )
    cmd = CreateRate(
        agency_name="test",
        to_currency=CurrencyCode.create("USD"),
        rate=Money.create(Decimal("1.25")),
    )
    handler = CreateRateHandler(FakeRepository[Agency]({agency}), FakeRepository[Rate]())

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_success()

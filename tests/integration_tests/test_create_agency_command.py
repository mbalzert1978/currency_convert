from currency_convert.core.app.agency.create.command import CreateAgency
from currency_convert.core.app.agency.create.handler import CreateAgencyHandler
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from tests.helper.fake_repository import FakeRepository


def test_agency_can_be_created_from_command_handler() -> None:
    # Arrange
    cmd = CreateAgency(
        name="test_agency",
        base_currency=CurrencyCode.create(),
        residing_country=Country.create(),
    )
    handler = CreateAgencyHandler(FakeRepository[Agency]())

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_success()


def test_failure_result_on_duplication():
    # Arrange
    agency = Agency.create(
        "test_agency",
        CurrencyCode.create(),
        Country.create(),
    )
    cmd = CreateAgency(
        name="test_agency",
        base_currency=CurrencyCode.create(),
        residing_country=Country.create(),
    )
    handler = CreateAgencyHandler(FakeRepository[Agency]({agency}))

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_failure()

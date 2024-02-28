from currency_convert.core.app.agency.update.command import UpdateAgency
from currency_convert.core.app.agency.update.handler import UpdateAgencyHandler
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from tests.helper.fake_repository import FakeRepository


def test_update_agency():
    # Arrange
    expected = "new_name"
    agency = Agency.create(
        "test_agency",
        CurrencyCode.create(),
        Country.create(),
    )
    cmd = UpdateAgency(id_=agency.id_, name=expected)
    repo = FakeRepository[Agency]({agency})
    handler = UpdateAgencyHandler(repo)

    # Act
    result = handler.handle(cmd)

    # Assert
    assert result.is_success()
    assert repo._entities.pop().name == expected

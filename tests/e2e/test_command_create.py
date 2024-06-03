from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.application.agency.commands.create.handler import (
    CreateAgencyHandler,
)
from currency_convert.domain.agency.entities.interface import AgencyRepository


def test_create_agency_command(EmptyAgencyRepository: AgencyRepository) -> None:
    cmd = CreateAgency("test", "foo", "bar", "baz")
    handler = CreateAgencyHandler(EmptyAgencyRepository)

    result = handler.execute(cmd)

    in_db = EmptyAgencyRepository.find_by_name("test").unwrap()
    assert result.is_ok()
    assert len(in_db.rates) == 0

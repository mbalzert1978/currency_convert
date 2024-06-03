from currency_convert.application.agency.commands.update.command import (
    UpdatebyName,
    UpdatebyId,
)
from currency_convert.application.agency.commands.update.handler import UpdateHandler
from currency_convert.domain.agency.entities.interface import (
    AgencyRepository,
    UpdateStrategy,
)


def test_update_command_by_name(
    MemoryStrategy: UpdateStrategy, MemoryAgencyRepository: AgencyRepository
) -> None:
    cmd = UpdatebyName(MemoryStrategy, "EZB")
    handler = UpdateHandler(MemoryAgencyRepository)

    result = handler.by_name(cmd)
    in_db = MemoryAgencyRepository.find_by_name("EZB").unwrap()
    assert result.is_ok()
    assert len(in_db.rates) == 3


def test_update_command_by_id(
    MemoryStrategy: UpdateStrategy, MemoryAgencyRepository: AgencyRepository
) -> None:
    first = next(iter(MemoryAgencyRepository.find_all().unwrap()))

    cmd = UpdatebyId(MemoryStrategy, first.id.hex)
    handler = UpdateHandler(MemoryAgencyRepository)

    result = handler.by_id(cmd)
    in_db = MemoryAgencyRepository.find_by_name("EZB").unwrap()
    assert result.is_ok()
    assert len(in_db.rates) == 3

from currency_convert.application.agency.commands.update.command import (
    UpdatebyName,
    UpdatebyId,
)
from currency_convert.application.agency.commands.update.handler import (
    ByIdUpdateHandler,
    ByNameUpdateHandler,
)
from currency_convert.domain.agency.entities.interface import (
    AgencyRepository,
    UpdateStrategy,
)


def test_update_command_by_name(
    MemoryStrategy: UpdateStrategy, EmptyAgencyRepository: AgencyRepository
) -> None:
    cmd = UpdatebyName(MemoryStrategy, "EZB")
    handler = ByNameUpdateHandler(EmptyAgencyRepository)

    result = handler.execute(cmd)

    in_db = EmptyAgencyRepository.find_by_name("EZB").unwrap()
    assert result.is_ok()
    assert len(in_db.rates) == 3


def test_update_command_by_id(
    MemoryStrategy: UpdateStrategy, EmptyAgencyRepository: AgencyRepository
) -> None:
    first = next(iter(EmptyAgencyRepository.find_all().unwrap()))

    cmd = UpdatebyId(MemoryStrategy, first.id.hex)
    handler = ByIdUpdateHandler(EmptyAgencyRepository)

    result = handler.execute(cmd)

    in_db = EmptyAgencyRepository.find_by_name("EZB").unwrap()
    assert result.is_ok()
    assert len(in_db.rates) == 3

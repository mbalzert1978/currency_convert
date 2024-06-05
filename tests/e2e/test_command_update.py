from currency_convert.application.agency.commands.update.command import (
    UpdateById,
    UpdateByName,
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
    cmd = UpdateByName(MemoryStrategy, "EZB")
    handler = ByNameUpdateHandler(EmptyAgencyRepository)

    handler.execute(cmd)

    in_db = EmptyAgencyRepository.find_by_name("EZB")
    assert len(in_db.rates) == 3


def test_update_command_by_id(
    MemoryStrategy: UpdateStrategy, EmptyAgencyRepository: AgencyRepository
) -> None:
    first = next(iter(EmptyAgencyRepository.find_all()))

    cmd = UpdateById(MemoryStrategy, first.id.hex)
    handler = ByIdUpdateHandler(EmptyAgencyRepository)

    handler.execute(cmd)

    in_db = EmptyAgencyRepository.find_by_name("EZB")
    assert len(in_db.rates) == 3

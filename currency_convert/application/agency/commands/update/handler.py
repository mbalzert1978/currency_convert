from currency_convert.application.agency.commands.update.command import (
    UpdateById,
    UpdateByName,
)
from currency_convert.domain.agency.entities.agency import (
    AgencyNotFoundError,
    UpdateError,
)
from currency_convert.domain.agency.entities.interface import (
    AgencyRepository,
)
from currency_convert.domain.primitives.valueobject import ValueObjectError


class ByNameUpdateHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, cmd: UpdateByName) -> None:
        if (agency := self.repository.find_by_name(cmd.name)) is None:
            raise AgencyNotFoundError()
        try:
            agency.update(rate_strategy=cmd.strategy)
        except ValueObjectError as exc:
            raise UpdateError.from_exc(exc)
        else:
            self.repository.save(agency)


class ByIdUpdateHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, cmd: UpdateById) -> None:
        if (agency := self.repository.find_by_id(cmd.id)) is None:
            raise AgencyNotFoundError()
        try:
            agency.update(rate_strategy=cmd.strategy)
        except ValueObjectError as exc:
            raise UpdateError.from_exc(exc)
        else:
            self.repository.save(agency)

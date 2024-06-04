from functools import partial

from results import Result

from currency_convert.application.agency.commands.update.command import (
    UpdatebyId,
    UpdatebyName,
)
from currency_convert.domain.agency.entities.agency import Agency, UpdateError
from currency_convert.domain.agency.entities.interface import AgencyRepository


class ByNameUpdateHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, cmd: UpdatebyName) -> Result[Agency, UpdateError]:
        return (
            self.repository.find_by_name(cmd.name)
            .and_then(partial(Agency.update, rate_strategy=cmd.strategy))
            .and_then(self.repository.save)
            .map_err(UpdateError.from_exc)
        )


class ByIdUpdateHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, cmd: UpdatebyId) -> Result[Agency, UpdateError]:
        return (
            self.repository.find_by_id(cmd.id)
            .and_then(partial(Agency.update, rate_strategy=cmd.strategy))
            .and_then(self.repository.save)
            .map_err(UpdateError.from_exc)
        )

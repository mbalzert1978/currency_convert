from functools import partial

from results import Result

from currency_convert.application.agency.commands.update.command import (
    UpdatebyId,
    UpdatebyName,
)
from currency_convert.domain.agency.entities.agency import Agency, UpdateError
from currency_convert.domain.agency.entities.interface import AgencyRepository


class UpdateHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def by_name(self, query: UpdatebyName) -> Result[Agency, UpdateError]:
        return (
            self.repository.find_by_name(query.name)
            .and_then(partial(Agency.update, rate_strategy=query.strategy))
            .and_then(self.repository.save)
            .map_err(UpdateError.from_exc)
        )

    def by_id(self, query: UpdatebyId) -> Result[Agency, UpdateError]:
        return (
            self.repository.find_by_id(query.id)
            .and_then(partial(Agency.update, rate_strategy=query.strategy))
            .and_then(self.repository.save)
            .map_err(UpdateError.from_exc)
        )

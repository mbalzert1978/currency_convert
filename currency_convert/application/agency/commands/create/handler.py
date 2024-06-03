from results import Result

from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.domain.agency.entities.agency import Agency, AgencyCreationError
from currency_convert.domain.agency.entities.interface import AgencyRepository


class CreateAgencyHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def __call__(self, cmd: CreateAgency) -> Result[Agency, AgencyCreationError]:
        if self.repository.find_by_name(cmd.name).is_ok():
            return Result.Err(AgencyCreationError("Agency already exists"))

        return (
            Agency.create(cmd.base, cmd.name, cmd.address, cmd.country)
            .and_then(self.repository.save)
            .map_err(AgencyCreationError.from_exc)
        )

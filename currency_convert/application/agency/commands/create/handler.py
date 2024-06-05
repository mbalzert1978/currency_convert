from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
    DuplicateAgencyError,
)
from currency_convert.domain.agency.entities.interface import AgencyRepository


class CreateAgencyHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, cmd: CreateAgency) -> Agency:
        try:
            agency = self.repository.find_by_name(cmd.name)
        except AgencyNotFoundError:
            agency = Agency.create(cmd.base, cmd.name, cmd.address, cmd.country)
            self.repository.save(agency)
            return agency
        raise DuplicateAgencyError(agency)

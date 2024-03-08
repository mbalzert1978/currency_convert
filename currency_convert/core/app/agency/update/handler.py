from http import HTTPStatus

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.agency.update.command import UpdateAgency
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.returns import (
    Failure,
    Null,
    Result,
    Some,
    Success,
)


class UpdateAgencyHandler(CommandHandler[UpdateAgency, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository) -> None:
        self._agency_repository = agency_repository

    def handle(self, cmd: UpdateAgency) -> Result[None, Error]:
        match err := self._agency_repository.get(cmd.id_):
            case Success(Some(agency)):
                return self._agency_repository.update(
                    agency, cmd.name, cmd.base_currency, cmd.residing_country
                )
            case Success(Null()):
                not_found = AgencyNotFoundError(
                    HTTPStatus.NOT_FOUND,
                    strings_error.NOT_FOUND % ("ID", cmd),
                )
                return Failure(not_found)
            case _:
                # Result contains an error.
                return err  # type: ignore[return-value]

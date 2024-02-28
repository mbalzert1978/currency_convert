from http import HTTPStatus

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.agency.update.command import UpdateAgency
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result

ERR_MESSAGE = "There is no Agency with the given id."


class UpdateAgencyHandler(CommandHandler[UpdateAgency, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository) -> None:
        self._agency_repository = agency_repository

    def handle(self, cmd: UpdateAgency) -> Result[None, Error]:
        with self._agency_repository as repo:
            get_result = repo.get(cmd.id_)

        if get_result.is_failure() or (maybe_agency := get_result.unwrap()).is_none():
            return Result.from_failure(AgencyNotFoundError(HTTPStatus.NOT_FOUND, ERR_MESSAGE))

        with self._agency_repository as repo:
            db_result = repo.update(maybe_agency.unwrap(), cmd.name, cmd.base_currency, cmd.residing_country)

        return db_result if db_result.is_failure() else Result.from_value(None)

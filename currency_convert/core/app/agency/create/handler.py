from http import HTTPStatus

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.agency.create.command import CreateAgency
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.agency.errors import AgencyAllreadExistsError
from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.returns import Result


class CreateAgencyHandler(CommandHandler[CreateAgency, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository) -> None:
        self._agency_repository = agency_repository

    def handle(self, cmd: CreateAgency) -> Result[None, Error]:
        with self._agency_repository as repo:
            get_result = repo.find_by_name(cmd.name)

        if get_result.is_success() and get_result.unwrap().is_some():
            return Result.from_failure(
                AgencyAllreadExistsError(
                    HTTPStatus.CONFLICT,
                    strings_error.ALREADY_EXIST % ("Agency", cmd.name),
                )
            )

        into_db = Agency.create(
            name=cmd.name,
            base_currency=cmd.base_currency,
            residing_country=cmd.residing_country,
        )

        with self._agency_repository as repo:
            db_result = repo.add(into_db)

        return db_result if db_result.is_failure() else Result.from_value(None)

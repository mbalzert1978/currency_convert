from http import HTTPStatus

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.rate.command import CreateRates
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
from currency_convert.core.domain.rate.rate_repository import IRateRepository
from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result


class CreateRatesHandler(CommandHandler[CreateRates, Result[None, Error]]):
    def __init__(
        self, agency_repository: IAgencyRepository, rate_repository: IRateRepository
    ) -> None:
        self._agency_repository = agency_repository
        self._rate_repository = rate_repository

    def handle(self, cmd: CreateRates) -> Result[None, Error]:
        if (
            get_result := self._agency_repository.find_by_name(cmd.agency_name)
        ).is_failure():
            return Result.from_failure(get_result.failure())
        if get_result.unwrap().is_none():
            return Result.from_failure(
                AgencyNotFoundError(
                    HTTPStatus.NOT_FOUND,
                    strings_error.NOT_FOUND % ("Name", cmd.agency_name),
                )
            )
        with self._rate_repository as repo:
            db_result = repo.add_many(cmd.rates)
        if db_result.is_failure():
            return Result.from_failure(db_result)
        return Result.from_value(None)

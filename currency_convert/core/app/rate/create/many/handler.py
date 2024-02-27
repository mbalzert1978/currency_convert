from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.many.command import CreateRates
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
from currency_convert.core.domain.rate.rate_repository import IRateRepository
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result

UNREACHABLE = Error(500, "Unreachable code.")
NOT_FOUND_MSG = "No agency with name: %s found."


class CreateRatesHandler(CommandHandler[CreateRates, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository, rate_repository: IRateRepository) -> None:
        self._agency_repository = agency_repository
        self._rate_repository = rate_repository

    def handle(self, cmd: CreateRates) -> Result[None, Error]:
        if self._agency_repository.find_by_name(cmd.agency_name).is_failure():
            return Result.from_failure(AgencyNotFoundError(404, NOT_FOUND_MSG % cmd.agency_name))
        with self._rate_repository as repo:
            db_result = repo.add_many(cmd.rates)
        if db_result.is_failure():
            return Result.from_failure(db_result)
        return Result.from_value(None)

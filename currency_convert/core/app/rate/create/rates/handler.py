from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.rates.command import CreateRate
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.rate.rate_repository import IRateRepository
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result


class CreateRateHandler(CommandHandler[CreateRate, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository, rate_repository: IRateRepository) -> None:
        self._agency_repository = agency_repository
        self._rate_repository = rate_repository

    def handle(self, cmd: CreateRate) -> Result[None, Error]:
        with self._agency_repository as repo:
            get_result = repo.find_by_name(cmd.agency_name)

        if get_result.is_failure() or (agency := get_result.unwrap()).is_none():
            return Result.from_failure(get_result.failure())

        in_rate = Rate.create(agency.unwrap().id_, cmd.to_currency, cmd.rate)
        with self._rate_repository as repo:
            write_result = repo.add(in_rate)
        return Result.from_value(None) if (write_result).is_success() else write_result

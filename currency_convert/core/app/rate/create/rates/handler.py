from http import HTTPStatus

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.rates.command import CreateRate
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.rate.rate_repository import IRateRepository
from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.returns import (
    Failure,
    Null,
    Result,
    Some,
    Success,
)


class CreateRateHandler(CommandHandler[CreateRate, Result[None, Error]]):
    def __init__(
        self,
        agency_repository: IAgencyRepository,
        rate_repository: IRateRepository,
    ) -> None:
        self._agency_repository = agency_repository
        self._rate_repository = rate_repository

    def handle(self, cmd: CreateRate) -> Result[None, Error]:
        match err := self._agency_repository.find_by_name(cmd.agency_name):
            case Success(Some(agency)):
                in_rate = Rate.create(agency.id_, cmd.to_currency, cmd.rate)
                return self._rate_repository.add(in_rate)
            case Success(Null()):
                not_found = AgencyNotFoundError(
                    HTTPStatus.NOT_FOUND,
                    strings_error.NOT_FOUND % (cmd.agency_name, cmd),
                )
                return Failure(not_found)
            case _:
                # Result contains an error.
                return err  # type: ignore[return-value]

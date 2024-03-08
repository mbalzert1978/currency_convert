from http import HTTPStatus

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.rate.command import CreateRates
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
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


class CreateRatesHandler(CommandHandler[CreateRates, Result[None, Error]]):
    def __init__(
        agency_repository: IAgencyRepository,
        rate_repository: IRateRepository,
    ) -> None:
        self._agency_repository = agency_repository
        self._rate_repository = rate_repository

    def handle(self, cmd: CreateRates) -> Result[None, Error]:
        match err := self._agency_repository.find_by_name(cmd.agency_name):
            case Success(Some(_)):
                return self._rate_repository.add_many(cmd.rates)
            case Success(Null()):
                not_found = AgencyNotFoundError(
                    HTTPStatus.NOT_FOUND,
                    strings_error.NOT_FOUND % (cmd.agency_name, cmd),
                )
                return Failure(not_found)
            case _:
                # Result contains an error.
                return err  # type: ignore[return-value]
from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.single.command import CreateRate
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.rate.rate_repository import IRateRepository
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Failure, Result, Success
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID

UNREACHABLE = Error(500, "Unreachable code.")


class CreateRateHandler(CommandHandler[CreateRate, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository, rate_repository: IRateRepository) -> None:
        self._agency_repository = agency_repository
        self._rate_repoitory = rate_repository

    def handle(self, cmd: CreateRate) -> Result[None, Error]:
        match self._agency_repository.find_by_name(cmd.agency_name):
            case Success(agency):
                return self._insert_rate(agency.id_, cmd)
            case Failure(_):
                in_agency = Agency.create(
                    name=cmd.agency_name,
                    base_currency=cmd.base_currency,
                    residing_country=cmd.residing_coutry,
                )
                with self._agency_repository as repo:
                    match repo.add(in_agency):
                        case Success(_):
                            return self._insert_rate(in_agency.id_, cmd)
                        case Failure(exc):
                            return Result.from_failure(exc)
                        case _:
                            return Result.from_failure(UNREACHABLE)
            case _:
                return Result.from_failure(UNREACHABLE)

    def _insert_rate(self, agency_id: UUIDID, cmd: CreateRate) -> Result[None, Error]:
        in_rate = Rate.create(agency_id, cmd.to_currency, cmd.rate)
        with self._rate_repoitory as repo:
            db_result = repo.add(in_rate)
        if db_result.is_failure():
            return Result.from_failure(db_result)
        return Result.from_value(None)

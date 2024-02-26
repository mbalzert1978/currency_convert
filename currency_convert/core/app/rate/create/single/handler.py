from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.rate.create.single.command import CreateRate
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.rate.rate_repository import IRateRepository
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class CreateRateHandler(CommandHandler[CreateRate, Result[None, Error]]):
    def __init__(self, agency_repository: IAgencyRepository, rate_repository: IRateRepository) -> None:
        self._agency_repository = agency_repository
        self._rate_repoitory = rate_repository

    def handle(self, cmd: CreateRate) -> Result[None, Error]:
        with self._agency_repository as repo:
            get_result = repo.find_by_name(cmd.agency_name)

        if (get_result).is_success() and (agency := get_result.unwrap()).is_some():
            return self._insert_rate(agency.unwrap().id_, cmd)

        in_agency = Agency.create(
            name=cmd.agency_name,
            base_currency=cmd.base_currency,
            residing_country=cmd.residing_coutry,
        )

        with self._agency_repository as repo:
            in_result = repo.add(in_agency)

        if (in_result).is_success():
            return self._insert_rate(in_agency.id_, cmd)
        return in_result

    def _insert_rate(self, agency_id: UUIDID, cmd: CreateRate) -> Result[None, Error]:
        in_rate = Rate.create(agency_id, cmd.to_currency, cmd.rate)
        with self._rate_repoitory as repo:
            write_result = repo.add(in_rate)
        return Result.from_value(None) if (write_result).is_success() else write_result

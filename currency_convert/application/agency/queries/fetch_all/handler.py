from results import Result

from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.domain.agency.entities.agency import Agency, AgencyNotFoundError
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate


class FetchAllHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, query: FetchAll) -> Result[tuple[Rate, ...], AgencyNotFoundError]:
        return (
            self.repository.find_by_name(query.agency_name)
            .and_then(Agency.get_rates)
            .map_err(AgencyNotFoundError.from_exc)
        )

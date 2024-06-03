from results import Result
from currency_convert.application.agency.queries.fetch_one.query import FetchOne
from currency_convert.domain.agency.entities.agency import RateNotFoundError
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate


class FetchOneHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, query: FetchOne) -> Result[Rate, RateNotFoundError]:
        return (
            self.repository.find_by_name(query.agency_name)
            .map_err(RateNotFoundError.from_exc)
            .and_then(
                lambda agency: agency.get_rate(
                    query.currency_from,
                    query.currency_to,
                    query.iso_date,
                )
            )
        )

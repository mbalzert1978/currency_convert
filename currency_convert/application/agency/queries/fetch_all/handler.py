from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.domain.agency.entities.agency import AgencyNotFoundError
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate


class FetchAllHandler:
    def __init__(self, repository: AgencyRepository) -> None:
        self.repository = repository

    def execute(self, query: FetchAll) -> tuple[Rate, ...]:
        if (agency := self.repository.find_by_name(query.agency_name)) is None:
            raise AgencyNotFoundError()
        return agency.get_rates()

from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.application.agency.queries.fetch_all.handler import (
    FetchAllHandler,
)
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate
from tests.data import INSERTS


def test_query_all_rates(MemoryAgencyRepository: AgencyRepository) -> None:
    expected = tuple(Rate.from_attributes(None, *rate.values()) for rate in INSERTS)
    cmd = FetchAll("EZB")
    handler = FetchAllHandler(MemoryAgencyRepository)
    result = handler.execute(cmd)
    assert result.is_ok()
    assert result.unwrap() == expected

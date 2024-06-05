from currency_convert.application.agency.queries.fetch_one.handler import (
    FetchOneHandler,
)
from currency_convert.application.agency.queries.fetch_one.query import FetchOne
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate
from tests.data import INSERTS


def test_query_one_rate(MemoryAgencyRepository: AgencyRepository) -> None:
    expected = Rate.from_attributes(None, *INSERTS[0].values())
    cmd = FetchOne("EZB", "EUR", "USD", "2020-01-01T00:00:00")
    handler = FetchOneHandler(MemoryAgencyRepository)
    result = handler.execute(cmd)
    assert result.is_ok()
    assert result.unwrap() == expected

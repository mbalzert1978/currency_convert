import datetime

from currency_convert.application.agency.queries.fetch_one.handler import (
    FetchOneHandler,
)
from currency_convert.application.agency.queries.fetch_one.query import FetchOne
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate
from tests.data import INSERTS


def test_query_one_rate(MemoryAgencyRepository: AgencyRepository) -> None:
    expected = Rate.create(
        currency_from=INSERTS[0]["currency_from"],
        currency_to=INSERTS[0]["currency_to"],
        rate=INSERTS[0]["rate"],
        dt=(to_get := datetime.datetime.fromisoformat(INSERTS[0]["date"])),
    )
    cmd = FetchOne("EZB", "EUR", "USD", to_get)
    handler = FetchOneHandler(MemoryAgencyRepository)
    assert handler.execute(cmd) == expected

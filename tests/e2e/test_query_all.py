import datetime

from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.application.agency.queries.fetch_all.handler import (
    FetchAllHandler,
)
from currency_convert.domain.agency.entities.interface import AgencyRepository
from currency_convert.domain.agency.valueobjects.rate import Rate
from tests.data import INSERTS


def test_query_all_rates(MemoryAgencyRepository: AgencyRepository) -> None:
    expected = tuple(
        Rate.create(
            currency_from=rate["currency_from"],
            currency_to=rate["currency_to"],
            rate=rate["rate"],
            dt=datetime.datetime.fromisoformat(rate["date"]),
        )
        for rate in sorted(INSERTS, key=lambda x: x["date"], reverse=True)
    )

    cmd = FetchAll("EZB", lambda _: True)
    handler = FetchAllHandler(MemoryAgencyRepository)

    assert handler.execute(cmd) == expected

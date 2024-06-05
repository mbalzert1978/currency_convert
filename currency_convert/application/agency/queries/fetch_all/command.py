import dataclasses
from typing import Callable

from currency_convert.application.primitives.query import Query
from currency_convert.domain.agency.valueobjects.rate import Rate


@dataclasses.dataclass(frozen=True)
class FetchAll(Query):
    agency_name: str
    predicate: Callable[[Rate], bool]

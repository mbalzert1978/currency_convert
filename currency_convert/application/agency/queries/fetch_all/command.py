import dataclasses

from currency_convert.application.primitives.query import Query


@dataclasses.dataclass(frozen=True)
class FetchAll(Query):
    agency_name: str

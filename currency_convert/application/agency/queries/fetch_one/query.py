import dataclasses
import datetime

from currency_convert.application.primitives.query import Query


@dataclasses.dataclass(frozen=True)
class FetchOne(Query):
    agency_name: str
    currency_from: str
    currency_to: str
    dt: datetime.datetime | None = None

import typing
from typing_extensions import TypedDict

from results import Result

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
)
from currency_convert.domain.agency.valueobjects.money import _Decimal


class UnprocessedRate(TypedDict):
    currency_from: str
    currency_to: str
    rate: _Decimal
    date: str


class UnprocessableRate(UnprocessedRate):
    pass


class UpdateStrategy(typing.Protocol):
    def __call__(self) -> list[UnprocessedRate]:
        pass


class AgencyRepository(typing.Protocol):
    def find_by_id(self, agency_id: str) -> Result[Agency, AgencyNotFoundError]:
        pass

    def find_by_name(self, name: str) -> Result[Agency, AgencyNotFoundError]:
        pass

    def find_all(self) -> Result[list[Agency], AgencyNotFoundError]:
        pass

    def save(self, agency: Agency) -> Result[Agency, Exception]:
        pass

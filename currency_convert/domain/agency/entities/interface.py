import typing

from typing_extensions import TypedDict

from currency_convert.domain.agency.entities.agency import Agency


class UnprocessedRate(TypedDict):
    currency_from: str
    currency_to: str
    rate: str
    date: str


class UnprocessableRate(UnprocessedRate):
    pass


class UpdateStrategy(typing.Protocol):
    def __call__(self) -> list[UnprocessedRate]: ...


class AgencyRepository(typing.Protocol):
    def find_by_id(self, agency_id: str) -> Agency: ...

    def find_by_name(self, name: str) -> Agency: ...

    def find_all(self) -> list[Agency]: ...

    def save(self, agency: Agency) -> None: ...

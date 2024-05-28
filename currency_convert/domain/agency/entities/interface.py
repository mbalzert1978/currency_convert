from typing import Protocol, Sequence

from result import Result

from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.domain.primitives.error import GenericError


class RatesRepository(Protocol):
    def add(self, rate: Rate) -> Result[None, GenericError]: ...

    def get_all(self) -> Result[Sequence[Rate], GenericError]: ...

from __future__ import annotations
import dataclasses
import typing

from result import Result

from currency_convert.domain.primitives.error import GenericError
from currency_convert.domain.primitives.valueobject import ValueObject

T = typing.TypeVar("T")


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Currency(ValueObject[str]):
    code: str

    @classmethod
    def create(cls, code: str) -> Result[Currency, GenericError]:
        if len(code) != 3:
            return Result.Err(GenericError())
        return Result.Ok(cls(code))

    def get_atomic_values(self) -> typing.Iterator[str]:
        yield self.code

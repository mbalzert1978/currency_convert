from __future__ import annotations

import dataclasses
import decimal
import typing
from typing import Iterator

from result import Result

from currency_convert.domain.primitives.error import GenericError
from currency_convert.domain.primitives.valueobject import ValueObject

_Decimal: typing.TypeAlias = (
    decimal.Decimal | float | str | tuple[int, typing.Sequence[int], int]
)
_PRECISION = decimal.Decimal(10) ** -8


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Money(ValueObject[decimal.Decimal]):
    value: decimal.Decimal

    def get_atomic_values(self) -> Iterator[decimal.Decimal]:
        yield self.value

    @classmethod
    def create(cls, value: _Decimal) -> Result[Money, GenericError]:
        try:
            r = cls(decimal.Decimal(value).quantize(_PRECISION).copy_abs())
        except decimal.InvalidOperation as exc:
            return Result.Err(GenericError.from_exc(exc))
        else:
            return Result.Ok(r)

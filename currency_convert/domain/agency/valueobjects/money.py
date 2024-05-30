from __future__ import annotations

import dataclasses
import decimal
import typing
from typing import Iterator

from results import Result

from currency_convert.domain.primitives.error import GenericError
from currency_convert.domain.primitives.valueobject import ValueObject

_Decimal: typing.TypeAlias = (
    decimal.Decimal | float | str | tuple[int, typing.Sequence[int], int]
)
_PRECISION = decimal.Decimal(10) ** -8


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Money(ValueObject[decimal.Decimal]):
    value: decimal.Decimal

    def get_values(self) -> Iterator[decimal.Decimal]:
        yield self.value

    @classmethod
    def create(cls, value: _Decimal) -> Result[typing.Self, GenericError]:
        try:
            v = decimal.Decimal(value).quantize(_PRECISION)
        except decimal.DecimalException as exc:
            return Result.Err(GenericError(exc))
        else:
            return Result.Ok(cls(v)) if v > 0 else Result.Err(GenericError())

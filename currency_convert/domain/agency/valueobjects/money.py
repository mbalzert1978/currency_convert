from __future__ import annotations

import dataclasses
import decimal
import typing
from typing import Iterator

from currency_convert.domain.primitives.error import GenericError
from currency_convert.domain.primitives.valueobject import ValueObject

_Decimal: typing.TypeAlias = (
    decimal.Decimal | float | str | tuple[int, typing.Sequence[int], int]
)


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Money(ValueObject[decimal.Decimal]):
    _PRECISION = dataclasses.field(default=decimal.Decimal(10) ** -8, init=False)
    value: decimal.Decimal

    def get_atomic_values(self) -> Iterator[decimal.Decimal]:
        yield self.value

    @classmethod
    def create(cls, value: _Decimal) -> Money:
        try:
            return cls(decimal.Decimal(value).quantize(cls._PRECISION).copy_abs())
        except decimal.InvalidOperation as exc:
            raise GenericError from exc

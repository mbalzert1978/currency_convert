from __future__ import annotations

import dataclasses
import decimal
import typing
from typing import Iterator

from results import Result

from currency_convert.domain.primitives.valueobject import ValueObject, ValueObjectError

_Decimal = decimal.Decimal | float | str | tuple[int, typing.Sequence[int], int]


class MoneyError(ValueObjectError):
    """Base class for errors related to Money."""


class FormatError(MoneyError):
    """Format error."""


class NegativeError(MoneyError):
    """Negative error."""


@dataclasses.dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class Money(ValueObject[decimal.Decimal]):
    PRECISION: typing.ClassVar[decimal.Decimal] = decimal.Decimal(10) ** -8
    ERROR_MSG: typing.ClassVar[str] = "Money value must be positive. Got: {{value}}"
    amount: decimal.Decimal

    def get_values(self) -> Iterator[decimal.Decimal]:
        yield self.amount

    @classmethod
    def create(
        cls, value: _Decimal
    ) -> Result[typing.Self, FormatError | NegativeError]:
        try:
            v = decimal.Decimal(value).quantize(cls.PRECISION)
        except decimal.DecimalException as exc:
            return Result.Err(FormatError.from_exc(exc))
        else:
            if cls.is_positive(v):
                return Result.Ok(cls(amount=v))
            return Result.Err(NegativeError(cls.ERROR_MSG.format(value=value)))

    @classmethod
    def is_positive(cls, value: decimal.Decimal) -> bool:
        return value > decimal.Decimal(0)

    def invert(self) -> _Decimal:
        return 1 / self.amount

    def multiply(self, other: Money) -> _Decimal:
        return self.amount * other.amount

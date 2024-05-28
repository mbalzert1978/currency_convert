from __future__ import annotations

import dataclasses
from typing import Iterator

from result import Result

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import Money, _Decimal
from currency_convert.domain.primitives.error import GenericError
from currency_convert.domain.primitives.valueobject import ValueObject


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Rate(ValueObject[Currency | Money | str]):
    currency_from: Currency
    currency_to: Currency
    rate: Money
    date: str

    def get_atomic_values(self) -> Iterator[Currency | Money | str]:
        yield self.currency_from
        yield self.currency_to
        yield self.rate
        yield self.date

    @classmethod
    def create(
        cls,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        date: str,
    ) -> Result[Rate, GenericError]:
        if (cf := Currency.create(currency_from)).is_err():
            return Result.Err(GenericError())
        if (ct := Currency.create(currency_to)).is_err():
            return Result.Err(GenericError())
        if (r := Money.create(rate)).is_err():
            return Result.Err(GenericError())
        instance = cls(cf.unwrap(), ct.unwrap(), r.unwrap(), date)
        return Result.Ok(instance)

    def get_rate(self) -> Money:
        return self.rate

    def invert_rate(self) -> Result[Rate, GenericError]:
        try:
            inverted_decimal = 1 / next(self.rate.get_atomic_values())
        except StopIteration:
            return Result.Err(GenericError())
        if (r := Money.create(inverted_decimal)).is_err():
            return Result.Err(GenericError())
        instance = Rate(self.currency_to, self.currency_from, r.unwrap(), self.date)
        return Result.Ok(instance)

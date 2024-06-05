from __future__ import annotations

import dataclasses
import datetime
import typing

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import Money
from currency_convert.domain.primitives.valueobject import ValueObject, ValueObjectError


class RateError(ValueObjectError):
    """Base class for errors related to Rate."""


class InvalidDateError(RateError):
    """Invalid date error."""


@dataclasses.dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class Rate(ValueObject[Currency | Money | datetime.datetime]):
    currency_from: Currency
    currency_to: Currency
    rate: Money
    dt: datetime.datetime

    def get_values(self) -> typing.Iterator[Currency | Money | datetime.datetime]:
        yield self.currency_from
        yield self.currency_to
        yield self.rate
        yield self.dt

    @classmethod
    def from_attributes(
        cls,
        id: int | None,
        currency_from: str,
        currency_to: str,
        rate: str,
        dt: datetime.datetime,
    ) -> typing.Self:
        return cls(
            id=id,
            currency_from=Currency.from_str(currency_from),
            currency_to=Currency.from_str(currency_to),
            rate=Money.from_str(rate),
            dt=dt,
        )

    @classmethod
    def create(
        cls,
        currency_from: str,
        currency_to: str,
        rate: str,
        dt: datetime.datetime,
    ) -> typing.Self:
        if not isinstance(dt, datetime.datetime):
            raise InvalidDateError()
        return cls(
            currency_from=Currency.from_str(currency_from),
            currency_to=Currency.from_str(currency_to),
            rate=Money.from_str(rate),
            dt=dt,
        )

    def multiply(self, other: Rate) -> Rate:
        return self.create(
            other.currency_from.code,
            self.currency_to.code,
            self.rate.multiply(other.rate),
            self.dt,
        )

    def invert(self) -> Rate:
        return self.create(
            self.currency_to.code,
            self.currency_from.code,
            self.rate.invert(),
            self.dt,
        )

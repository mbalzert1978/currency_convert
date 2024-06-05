from __future__ import annotations

import dataclasses
import datetime
import typing

from results import Result

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import Money, _Decimal
from currency_convert.domain.primitives.valueobject import ValueObject, ValueObjectError


class RateError(ValueObjectError):
    """Base class for errors related to Rate."""


class InvalidRateError(RateError):
    """Error raised when an invalid rate is provided."""


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
        rate: _Decimal,
        dt: datetime.datetime,
    ) -> typing.Self:
        return cls(
            id=id,
            currency_from=Currency.create(currency_from).unwrap(),
            currency_to=Currency.create(currency_to).unwrap(),
            rate=Money.create(rate).unwrap(),
            dt=dt,
        )

    @classmethod
    def create(
        cls,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        dt: datetime.datetime,
    ) -> Result[typing.Self, ValueObjectError]:
        def create_currency_pair(
            currency: Currency,
        ) -> Result[tuple[Currency, Currency], ValueObjectError]:
            return Currency.create(currency_to).map(lambda ct: (currency, ct))

        def create_rate(
            currencies: tuple[Currency, Currency],
        ) -> Result[tuple[Currency, Currency, Money], ValueObjectError]:
            return Money.create(rate).map(lambda m: (*currencies, m))

        def is_valid_datetime(
            rate: tuple[Currency, Currency, Money],
        ) -> Result[
            tuple[Currency, Currency, Money, datetime.datetime],
            ValueObjectError,
        ]:
            if isinstance(dt, datetime.datetime):
                return Result.Ok((*rate, dt))
            return Result.Err(InvalidRateError("Invalid datetime provided"))

        return (
            Currency.create(currency_from)
            .and_then(create_currency_pair)
            .and_then(create_rate)
            .and_then(is_valid_datetime)
            .map(
                lambda rate: cls(
                    currency_from=rate[0],
                    currency_to=rate[1],
                    rate=rate[2],
                    dt=dt,
                )
            )
        )

    def multiply(self, other: Rate) -> Result[Rate, ValueObjectError]:
        return self.create(
            other.currency_from.code,
            self.currency_to.code,
            self.rate.multiply(other.rate),
            self.dt,
        )

    def invert(self) -> Result[Rate, ValueObjectError]:
        return self.create(
            self.currency_to.code,
            self.currency_from.code,
            self.rate.invert(),
            self.dt,
        )

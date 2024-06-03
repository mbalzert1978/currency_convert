from __future__ import annotations

import dataclasses
import datetime
import typing
from typing import Iterator

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
    date: datetime.datetime

    def get_values(self) -> Iterator[Currency | Money | datetime.datetime]:
        yield self.currency_from
        yield self.currency_to
        yield self.rate
        yield self.date

    @classmethod
    def from_attributes(
        cls,
        id: int | None,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        iso_str: str,
    ) -> typing.Self:
        return cls(
            id=id,
            currency_from=Currency.create(currency_from).unwrap(),
            currency_to=Currency.create(currency_to).unwrap(),
            rate=Money.create(rate).unwrap(),
            date=datetime.datetime.fromisoformat(iso_str),
        )

    @classmethod
    def create(
        cls,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        iso_str: str,
    ) -> Result[typing.Self, InvalidRateError]:
        def create_currency_pair(
            currency: Currency,
        ) -> Result[tuple[Currency, Currency], InvalidRateError]:
            return (
                Currency.create(currency_to)
                .map_err(InvalidRateError.from_exc)
                .map(lambda ct: (currency, ct))
            )

        def create_rate(
            currencies: tuple[Currency, Currency],
        ) -> Result[tuple[Currency, Currency, Money], InvalidRateError]:
            return (
                Money.create(rate)
                .map_err(InvalidRateError.from_exc)
                .map(lambda m: (*currencies, m))
            )

        def create_datetime(
            rate: tuple[Currency, Currency, Money],
        ) -> Result[
            tuple[Currency, Currency, Money, datetime.datetime],
            InvalidRateError,
        ]:
            return (
                Result.from_fn(datetime.datetime.fromisoformat, iso_str)
                .map_err(InvalidRateError.from_exc)
                .map(lambda dt: (*rate, dt))
            )

        return (
            Currency.create(currency_from)
            .map_err(InvalidRateError.from_exc)
            .and_then(create_currency_pair)
            .and_then(create_rate)
            .and_then(create_datetime)
            .map(
                lambda rate: cls(
                    currency_from=rate[0],
                    currency_to=rate[1],
                    rate=rate[2],
                    date=rate[3],
                )
            )
        )

    def multiply(self, other: Rate) -> Result[Rate, InvalidRateError]:
        return self.create(
            other.currency_from.code,
            self.currency_to.code,
            self.rate.multiply(other.rate),
            self.date.isoformat(),
        )

    def invert(self) -> Result[Rate, InvalidRateError]:
        return self.create(
            self.currency_to.code,
            self.currency_from.code,
            self.rate.invert(),
            self.date.isoformat(),
        )

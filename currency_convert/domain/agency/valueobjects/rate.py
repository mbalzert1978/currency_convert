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


class InvalidDateError(RateError):
    """Invalid date error."""


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
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
    def create(
        cls,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        iso_str: str,
    ) -> Result[typing.Self, ValueObjectError]:
        def create_currency_pair(
            currency: Currency,
        ) -> Result[tuple[Currency, Currency], ValueObjectError]:
            return Currency.create(currency_to).map(lambda ct: (currency, ct))

        def create_rate(
            currencies: tuple[Currency, Currency],
        ) -> Result[tuple[Currency, Currency, Money], ValueObjectError]:
            return Money.create(rate).map(lambda m: (*currencies, m))

        def create_datetime(
            rate: tuple[Currency, Currency, Money],
        ) -> Result[
            tuple[Currency, Currency, Money, datetime.datetime],
            ValueObjectError,
        ]:
            return (
                Result.as_result(datetime.datetime.fromisoformat)(iso_str)
                .map_err(lambda exc: InvalidDateError.from_exc(exc))  # type: ignore [return-value]
                .map(lambda dt: (*rate, dt))
            )

        return (
            Currency.create(currency_from)
            .and_then(create_currency_pair)
            .and_then(create_rate)
            .and_then(create_datetime)
            .map(lambda rate: cls(*rate))
        )

    def multiply(self, other: Rate) -> Result[Rate, ValueObjectError]:
        return self.create(
            other.currency_from.code,
            self.currency_to.code,
            self.rate.multiply(other.rate),
            self.date.isoformat(),
        )

    def invert(self) -> Result[Rate, ValueObjectError]:
        return self.create(
            self.currency_to.code,
            self.currency_from.code,
            self.rate.invert(),
            self.date.isoformat(),
        )

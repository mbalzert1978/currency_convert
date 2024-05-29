from __future__ import annotations

import dataclasses
import logging
import typing
from typing import Never, Sequence

from option import Option, Some
from result import Err, Result
from typing_extensions import TypedDict

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import _Decimal
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.domain.primitives.entity import AggregateRoot

from ...primitives.error import GenericError

_logger = logging.getLogger(__name__)


class UnprocessedRate(TypedDict):
    currency_from: str
    currency_to: str
    rate: _Decimal
    date: str


class UnprocessableRate(UnprocessedRate):
    pass


TIME_PERIOD = 5


@dataclasses.dataclass(slots=True, eq=False)
class Agency(AggregateRoot):
    base: Currency
    name: str
    country: str
    rates: list[Rate] = dataclasses.field(default_factory=list)

    def add_rate(
        self, currency_from: str, currency_to: str, rate: _Decimal, date: str
    ) -> Result[None, Never]:
        return Rate.create(currency_from, currency_to, rate, date).and_then(
            Result.as_result(self.rates.append)
        )

    def add_rates(
        self, rates: list[UnprocessedRate]
    ) -> Result[None, list[UnprocessableRate]]:
        unprocessable = [
            rate
            for rate in rates
            if Rate.create(
                rate["currency_from"], rate["currency_to"], rate["rate"], rate["date"]
            )
            .and_then(Result.as_result(self.rates.append))
            .is_err()
        ]
        return Result.Err(unprocessable) if unprocessable else Result.Ok(None)

    def get_rate(
        self, currency_from: str, currency_to: str, date: str
    ) -> Result[Rate, GenericError]:
        if currency_from == self.base.code:
            return (
                next((Some(r) for r in self.rates))
                .filter(lambda r: r.currency_to.code == currency_to)
                .ok_or_else(GenericError)
            )
        elif currency_to == self.base.code:
            return (
                next((Some(r) for r in self.rates))
                .filter(lambda r: r.currency_to.code == currency_from)
                .map(lambda r: r.invert_rate().ok())
                .ok_or_else(GenericError)
            )
        else:
            if (
                rate_from := self.iter(lambda r: r.currency_to.code == currency_from)
            ).is_null():
                return rate_from.ok_or_else(GenericError)

            if (
                rate_to := self.iter(lambda r: r.currency_to.code == currency_to)
            ).is_null():
                return rate_to.ok_or_else(GenericError)

            return rate_from.map(
                Result.as_result(rate_to.unwrap().multiply)
            ).map_or_else(lambda: Err(GenericError()), lambda r: r)

    def iter(
        self,
        predicate: typing.Callable[[Rate], bool],
    ) -> Option[Rate, typing.Any]:
        return next(Some(r) for r in self.rates if predicate(r))

    @Result.as_result
    def list_rates(self) -> Sequence[Rate]:
        return tuple(self.rates)

    def _has_base(self, currency_from: str, currency_to: str) -> bool:
        return currency_from == self.base.code or currency_to == self.base.code

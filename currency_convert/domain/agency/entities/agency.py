from __future__ import annotations

import dataclasses
import logging
import typing
from typing import Never, Sequence

from results import Err, Null, Option, Result, Some
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
            if self.add_rate(
                rate["currency_from"], rate["currency_to"], rate["rate"], rate["date"]
            ).is_err()
        ]
        return Result.Err(unprocessable) if unprocessable else Result.Ok(None)

    def get_rate(
        self, currency_from: str, currency_to: str, date: str
    ) -> Result[Rate, GenericError]:
        if currency_from == self.base.code:
            return self.iter(lambda r: r.currency_to == currency_to).ok_or_else(
                GenericError
            )
        elif currency_to == self.base:
            return (
                self.iter(lambda r: r.currency_to == currency_from)
                .and_then(lambda r: r.invert_rate().ok())
                .ok_or_else(GenericError)
            )
        else:
            return (
                self.iter(lambda r: r.currency_to == currency_from)
                .ok_or_else(GenericError)
                .and_then(lambda r: r.invert_rate().map_err(GenericError))
                .and_then(
                    lambda rf: self.iter(lambda r: r.currency_to == currency_to)
                    .ok_or_else(GenericError)
                    .and_then(lambda rt: rt.multiply(rf).map_err(GenericError))
                )
            )

    def iter(
        self,
        predicate: typing.Callable[[Rate], bool],
    ) -> Option[Rate, typing.Any]:
        try:
            return next(Some(r) for r in self.rates if predicate(r))
        except StopIteration:
            return Null(None)

    @Result.as_result
    def list_rates(self) -> Sequence[Rate]:
        return tuple(self.rates)

    def _has_base(self, currency_from: str, currency_to: str) -> bool:
        return currency_from == self.base.code or currency_to == self.base.code

from __future__ import annotations

import dataclasses
import logging
import typing
from datetime import datetime
from functools import partial

from results import Null, Result, Some
from typing_extensions import TypedDict

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import _Decimal
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.domain.primitives.entity import AggregateRoot, EntityError

_logger = logging.getLogger(__name__)


class AgencyError(EntityError):
    """Base class for errors related to Agency."""


class AgencyNotFoundError(AgencyError):
    """Error raised when an agency is not found."""


class DuplicateRateError(AgencyError):
    """Error raised when a duplicate rate is added to an agency."""


class InvalidRateError(AgencyError):
    """Error raised when an invalid rate is provided."""


class InvalidCurrencyError(AgencyError):
    """Error raised when an invalid currency is provided."""


class RateNotFoundError(AgencyError):
    """Error raised when a rate is not found for the given criteria."""


class UnprocessedRate(TypedDict):
    currency_from: str
    currency_to: str
    rate: _Decimal
    date: str


class UnprocessableRate(UnprocessedRate):
    pass


@dataclasses.dataclass(slots=True, eq=False)
class Agency(AggregateRoot):
    base: Currency
    name: str
    address: str
    country: str
    rates: list[Rate] = dataclasses.field(default_factory=list)

    def add_rate(
        self,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        date: str,
    ) -> Result[Null[None], DuplicateRateError]:
        return (
            Rate.create(currency_from, currency_to, rate, date)
            .and_then(Result.as_result(self.rates.append))
            .map_err(lambda exc: DuplicateRateError.from_exc(exc))
            .map(Null)
        )

    def add_rates(
        self,
        rates: list[UnprocessedRate],
    ) -> Result[Null[None], list[UnprocessableRate]]:
        unprocessable = [
            rate
            for rate in rates
            if self.add_rate(
                rate["currency_from"],
                rate["currency_to"],
                rate["rate"],
                rate["date"],
            ).is_err()
        ]
        return Result.Err(unprocessable) if unprocessable else Result.Ok(Null(None))

    def get_rate(
        self,
        currency_from: str,
        currency_to: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Result[Rate, RateNotFoundError]:
        def filter_on(
            currency: str,
            start_date: str,
            end_date: str,
            r: Some[Rate],
        ) -> bool:
            return r.is_some_and(
                lambda r: (
                    r.currency_to == currency
                    and start_date <= r.date.isoformat() <= end_date
                )
            )

        def fetch_one(
            currency: str,
            start_date: str,
            end_date: str,
        ) -> Result[Rate, RateNotFoundError]:
            fn = partial(filter_on, currency, start_date, end_date)
            return (
                Result.as_result(lambda it: next(it))(filter(fn, self.iter()))
                .and_then(lambda sr: sr.ok_or_else(RateNotFoundError))
                .map_err(RateNotFoundError)
            )

        if start_date is None:
            start_date = datetime.now().isoformat()
        if end_date is None:
            end_date = datetime.now().isoformat()

        if self.is_base_currency(currency_from):
            return fetch_one(currency_to, start_date, end_date)
        if self.is_base_currency(currency_to):
            return (
                fetch_one(currency_from, start_date, end_date)
                .and_then(Rate.invert)  # type: ignore [arg-type]
                .map_err(RateNotFoundError)
            )
        return (
            fetch_one(currency_from, start_date, end_date)
            .and_then(Rate.invert)  # type: ignore [arg-type]
            .and_then(
                lambda rf: fetch_one(currency_to, start_date, end_date).and_then(
                    partial(Rate.multiply, other=rf)  # type: ignore [arg-type]
                )
            )
        ).map_err(RateNotFoundError.from_exc)

    def iter(self) -> typing.Iterator[Some[Rate]]:
        return (Some(r) for r in self.rates)

    def list_rates(self) -> Result[typing.Sequence[Some[Rate]], AgencyError]:
        return Result.as_result(tuple)(self.rates).map_err(AgencyError)  # type: ignore [return-value, arg-type]

    def is_base_currency(self, currency: str) -> bool:
        return currency == self.base

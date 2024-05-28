from __future__ import annotations

import dataclasses
import logging
from typing import Sequence

from result import Result
from typing_extensions import TypedDict

from currency_convert.domain.agency.entities.interface import RatesRepository
from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import _Decimal
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.domain.primitives.entity import AggregateRoot
from currency_convert.domain.primitives.error import GenericError

_logger = logging.getLogger(__name__)

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
    country: str
    rates_repository: RatesRepository

    def add_rate(
        self,
        currency_from: str,
        currency_to: str,
        rate: _Decimal,
        date: str,
    ) -> Result[None, GenericError]:
        if (r := Rate.create(currency_from, currency_to, rate, date)).is_err():
            return Result.Err(GenericError())
        return self.rates_repository.add(r.unwrap())

    def add_rates(
        self, rates: list[UnprocessedRate]
    ) -> Result[None, list[UnprocessableRate]]:
        unprocessable_rates = []
        for rate in rates:
            try:
                if (
                    r := Rate.create(
                        rate["currency_from"],
                        rate["currency_to"],
                        rate["rate"],
                        rate["date"],
                    )
                ).is_err():
                    _logger.error(f"Invalid rate: {rate}")
                    unprocessable_rates.append(rate)
                    continue
                self.rates_repository.add(r.unwrap())
            except KeyError:
                unprocessable_rates.append(rate)
        if unprocessable_rates:
            return Result.Err(unprocessable_rates)
        return Result.Ok(None)

    def _get_direct_rate(
        self, currency_from: str, currency_to: str, date: str
    ) -> Result[Rate, GenericError]:
        if (rates := self.rates_repository.get_all()).is_err():
            return Result.Err(GenericError())
        return next(
            (
                Result.Ok(rate)
                for rate in rates.unwrap()
                if rate.currency_from.code == currency_from
                and rate.currency_to.code == currency_to
                and rate.date == date
            ),
            Result.Err(GenericError()),
        )

    def _find_base_rates(
        self, currency_from: str, currency_to: str, date: str
    ) -> tuple[Rate | None, Rate | None]:
        if (rates := self.rates_repository.get_all()).is_err():
            return None, None

        rate_from_base = None
        rate_to_base = None

        for rate in rates.unwrap():
            match (rate.currency_from.code, rate.currency_to.code, rate.date):
                case (cf, self.base.code, d) if cf == currency_from and d == date:
                    rate_from_base = rate
                case (self.base.code, ct, d) if ct == currency_to and d == date:
                    rate_to_base = rate

        return rate_from_base, rate_to_base

    def get_rate(
        self,
        currency_from: str,
        currency_to: str,
        date: str,
    ) -> Result[Rate, GenericError]:
        if self._has_base(currency_from, currency_to):
            return self._get_direct_rate(currency_from, currency_to, date)

        rate_from_base, rate_to_base = self._find_base_rates(
            currency_from, currency_to, date
        )

        if rate_from_base is None or rate_to_base is None:
            return Result.Err(GenericError())

        try:
            compute_rate = next(rate_from_base.rate.get_atomic_values()) * next(
                rate_to_base.rate.get_atomic_values()
            )
        except StopIteration:
            return Result.Err(GenericError())

        if (i := Rate.create(currency_from, currency_to, compute_rate, date)).is_err():
            return Result.Err(GenericError())
        return Result.Ok(i.unwrap())

    def list_rates(self) -> Result[Sequence[Rate], GenericError]:
        if (rates := self.rates_repository.get_all()).is_err():
            return Result.Err(GenericError())
        return Result.Ok(rates.unwrap())

    def _has_base(self, currency_from: str, currency_to: str) -> bool:
        return currency_from == self.base.code or currency_to == self.base.code
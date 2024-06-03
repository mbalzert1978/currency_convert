from __future__ import annotations

import dataclasses
import typing
import uuid
from datetime import datetime
from functools import partial

from results import Err, Null, Ok, Result

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import _Decimal
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.domain.primitives.entity import AggregateRoot, EntityError

if typing.TYPE_CHECKING:
    from currency_convert.domain.agency.entities.interface import UpdateStrategy


class AgencyCreationError(EntityError):
    """Error raised when an agency cannot be created."""


class AgencyNotFoundError(EntityError):
    """Error raised when an agency is not found."""


class DuplicateRateError(EntityError):
    """Error raised when a duplicate rate is added to an agency."""


class RateNotFoundError(EntityError):
    """Error raised when a rate is not found for the given criteria."""


class UpdateError(EntityError):
    """Error raised when an agency cannot be updated."""


@dataclasses.dataclass(slots=True, eq=False)
class Agency(AggregateRoot):
    name: str
    base: Currency
    address: str
    country: str
    rates: list[Rate] = dataclasses.field(default_factory=list)

    @classmethod
    def from_attributes(
        cls,
        id: str,
        base: str,
        name: str,
        address: str,
        country: str,
        rates: list[Rate],
    ) -> typing.Self:
        return cls(
            id=uuid.UUID(id),
            base=Currency.create(base).unwrap(),
            name=name,
            address=address,
            country=country,
            rates=rates,
        )

    @classmethod
    def create(
        cls, base: str, name: str, address: str, country: str
    ) -> Result[Agency, AgencyCreationError]:
        return (
            Currency.create(base)
            .map(
                lambda base: cls(
                    id=uuid.uuid4(),
                    base=base,
                    name=name,
                    address=address,
                    country=country,
                )
            )
            .map_err(AgencyCreationError.from_exc)
        )

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
            .map_err(DuplicateRateError.from_exc)
            .map(Null)
        )

    def update(
        self,
        rate_strategy: UpdateStrategy,
    ) -> Result[Agency, UpdateError]:
        for rate in rate_strategy():
            match self.add_rate(
                rate["currency_from"],
                rate["currency_to"],
                rate["rate"],
                rate["date"],
            ):
                case Ok(_):
                    continue
                case Err(exc):
                    return Err(UpdateError.from_exc(exc))
        return Ok(self)

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
            r: Rate,
        ) -> bool:
            return (
                r.currency_to == currency
                and start_date <= r.date.isoformat() <= end_date
            )

        def fetch_one(
            currency: str,
            start_date: str,
            end_date: str,
        ) -> Result[Rate, Exception]:
            fn = partial(filter_on, currency, start_date, end_date)
            return Result.from_fn(next, filter(fn, self.rates))

        start_date = start_date or datetime.now().isoformat()
        end_date = end_date or datetime.now().isoformat()

        if self._is_base_currency(currency_from):
            return fetch_one(currency_to, start_date, end_date).map_err(
                RateNotFoundError.from_exc
            )
        if self._is_base_currency(currency_to):
            return (
                fetch_one(currency_from, start_date, end_date)
                .and_then(Rate.invert)  # type: ignore[arg-type]
                .map_err(RateNotFoundError.from_exc)
            )
        return (
            fetch_one(currency_from, start_date, end_date)
            .and_then(Rate.invert)  # type: ignore[arg-type]
            .and_then(
                lambda rf: fetch_one(currency_to, start_date, end_date).and_then(
                    partial(Rate.multiply, other=rf)  # type: ignore[arg-type]
                )
            )
        ).map_err(RateNotFoundError.from_exc)

    def get_rates(self) -> Result[tuple[Rate, ...], Exception]:
        result: Result[tuple[Rate, ...], Exception] = Result.from_fn(tuple, self.rates)
        return result

    def _is_base_currency(self, currency: str) -> bool:
        return currency == self.base

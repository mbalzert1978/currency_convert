from __future__ import annotations

import dataclasses
import datetime
import typing
import uuid
from functools import partial

from results import Err, Null, Ok, Result

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import _Decimal
from currency_convert.domain.agency.valueobjects.rate import InvalidRateError, Rate
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
    rates: set[Rate] = dataclasses.field(default_factory=set)

    @classmethod
    def from_attributes(
        cls,
        id: str,
        base: str,
        name: str,
        address: str,
        country: str,
        rates: set[Rate],
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
    ) -> Result[Null[None], InvalidRateError]:
        return (
            Result.from_fn(datetime.datetime.fromisoformat, date)
            .map_err(InvalidRateError.from_exc)
            .and_then(partial(Rate.create, currency_from, currency_to, rate))
            .map(self.rates.add)
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
        dt: datetime.datetime | None = None,
    ) -> Result[Rate, RateNotFoundError]:
        def filter_on_base_currency(r: Rate) -> bool:
            return r.currency_to == currency_to and (dt is None or dt == r.dt)

        def filter_on_inverted_currency(r: Rate) -> bool:
            return r.currency_to == currency_from and (dt is None or dt == r.dt)

        if self._is_base_currency(currency_from):
            return (
                self.get_rates(filter_on_base_currency)
                .map(iter)
                .and_then(
                    lambda iter: Result.from_fn(next, iter).map_err(
                        RateNotFoundError.from_exc
                    )
                )
            )
        if self._is_base_currency(currency_to):
            return (
                self.get_rates(filter_on_inverted_currency)
                .map(iter)
                .and_then(
                    lambda iter: Result.from_fn(next, iter).map_err(
                        RateNotFoundError.from_exc
                    )
                )
                .and_then(Rate.invert)
            )

        return (
            self.get_rates(filter_on_inverted_currency)
            .map(iter)
            .and_then(
                lambda iter: Result.from_fn(next, iter).map_err(
                    RateNotFoundError.from_exc
                )
            )
            .and_then(Rate.invert)
            .and_then(
                lambda rf: self.get_rates(filter_on_base_currency)
                .map(iter)
                .and_then(
                    lambda iter: Result.from_fn(next, iter).map_err(
                        RateNotFoundError.from_exc
                    )
                )
                .and_then(partial(Rate.multiply, other=rf))
            )
        )

    def get_rates(
        self,
        predicate: typing.Callable[[Rate], bool] = lambda r: True,
    ) -> Result[tuple[Rate, ...], RateNotFoundError]:
        return Result.from_fn(
            tuple,
            filter(predicate, sorted(self.rates, key=lambda r: r.dt, reverse=True)),
        ).map_err(RateNotFoundError.from_exc)

    def _is_base_currency(self, currency: str) -> bool:
        return currency == self.base

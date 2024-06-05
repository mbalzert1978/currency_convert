from __future__ import annotations

import dataclasses
import datetime
import typing
import uuid

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.domain.primitives.entity import AggregateRoot, EntityError

if typing.TYPE_CHECKING:
    from currency_convert.domain.agency.entities.interface import UpdateStrategy


class AgencyCreationError(EntityError):
    """Error raised when an agency cannot be created."""


class AgencySaveError(EntityError):
    """Error raised when an agency cannot be saved."""


class AgencyNotFoundError(EntityError):
    """Error raised when an agency is not found."""


class DuplicateAgencyError(EntityError):
    """Error raised when an agency with the same name already exists."""


class DuplicateRateError(EntityError):
    """Error raised when a duplicate rate is added to an agency."""


class RateNotFoundError(EntityError):
    """Error raised when a rate is not found for the given criteria."""


class UpdateError(EntityError):
    """Error raised when an agency cannot be updated."""


class RepositoryError(EntityError):
    """Base class for errors related to AgencyRepository."""


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
            base=Currency.from_str(base),
            name=name,
            address=address,
            country=country,
            rates=rates,
        )

    @classmethod
    def create(cls, base: str, name: str, address: str, country: str) -> Agency:
        return cls(
            id=uuid.uuid4(),
            base=Currency.from_str(base),
            name=name,
            address=address,
            country=country,
        )

    def add_rate(
        self,
        currency_from: str,
        currency_to: str,
        rate: str,
        date: str,
    ) -> None:
        self.rates.add(
            Rate.create(
                currency_from=currency_from,
                currency_to=currency_to,
                rate=rate,
                dt=datetime.datetime.fromisoformat(date),
            )
        )

    def update(self, rate_strategy: UpdateStrategy) -> None:
        for rate in rate_strategy():
            self.add_rate(**rate)

    def get_rate(
        self,
        currency_from: str,
        currency_to: str,
        dt: datetime.datetime | None = None,
    ) -> Rate:
        def filter_on_base_currency(r: Rate) -> bool:
            return r.currency_to == currency_to and (dt is None or dt == r.dt)

        def filter_on_inverted_currency(r: Rate) -> bool:
            return r.currency_to == currency_from and (dt is None or dt == r.dt)

        try:
            if self._is_base_currency(currency_from):
                return next(iter(self.get_rates(filter_on_base_currency)))
            if self._is_base_currency(currency_to):
                return next(iter(self.get_rates(filter_on_inverted_currency))).invert()

            return next(iter(self.get_rates(filter_on_base_currency))).multiply(
                next(iter(self.get_rates(filter_on_inverted_currency))).invert()
            )
        except StopIteration:
            msg = "No rate with the given criteria found."
            raise RateNotFoundError(msg)

    def get_rates(
        self,
        predicate: typing.Callable[[Rate], bool] = lambda _: True,
    ) -> tuple[Rate, ...]:
        return tuple(
            filter(predicate, sorted(self.rates, key=lambda r: r.dt, reverse=True)),
        )

    def _is_base_currency(self, currency: str) -> bool:
        return currency == self.base

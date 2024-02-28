import typing

import pydantic

from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import CreatedAtMixin, UpdatedAtMixin
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode


class Agency(Entity, CreatedAtMixin, UpdatedAtMixin):
    name: str
    base_currency: CurrencyCode
    residing_country: Country
    rates: set[Rate] = pydantic.Field(default_factory=set)

    @classmethod
    def create(
        cls,
        name: str,
        base_currency: CurrencyCode,
        residing_country: Country,
    ) -> typing.Self:
        return cls(
            name=name,
            base_currency=base_currency,
            residing_country=residing_country,
            created_at=None,
            updated_at=None,
        )

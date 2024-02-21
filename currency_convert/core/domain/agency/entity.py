import datetime
import typing

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import (
    CurrencyCode,
)


class Agency(Entity, DateTimeMixin):
    name: str
    base_currency: CurrencyCode
    residing_country: Country

    @classmethod
    def create(
        cls,
        name: str,
        base_currency: str,
        residing_country: str,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> typing.Self:
        return cls(
            name=name,
            base_currency=CurrencyCode.create(base_currency),
            residing_country=Country.create(residing_country),
            created_at=created_at,
            updated_at=updated_at,
        )

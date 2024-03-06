import datetime
import typing

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import CreatedAtMixin
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class Rate(Entity, CreatedAtMixin):
    agency_id: UUIDID  # type:ignore[type-arg]
    to_currency: CurrencyCode
    rate: Money

    @classmethod
    def create(
        cls,
        agency_id: UUIDID,  # type:ignore[type-arg]
        to_currency: CurrencyCode,
        rate: Money,
        created_at: datetime.datetime | None = None,
    ) -> typing.Self:
        return cls(
            agency_id=agency_id,
            to_currency=to_currency,
            rate=rate,
            created_at=created_at,
        )

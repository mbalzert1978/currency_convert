import datetime
import decimal
import typing

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin
from currency_convert.core.domain.shared.value_objects.money import Money


class Rate(Entity, DateTimeMixin):
    rate: Money

    @classmethod
    def create(
        cls,
        rate: decimal.Decimal,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> typing.Self:
        value = Money.create(rate)
        return cls(rate=value, created_at=created_at, updated_at=updated_at)

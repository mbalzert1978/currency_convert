import datetime
import typing

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin
from currency_convert.core.domain.shared.value_objects.currency_code import (
    CurrencyCode,
)


class Agency(Entity, DateTimeMixin):
    base_currency: CurrencyCode

    @classmethod
    def create(
        cls,
        code: str,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> typing.Self:
        value = CurrencyCode.create(code)
        return cls(
            base_currency=value,
            created_at=created_at,
            updated_at=updated_at,
        )

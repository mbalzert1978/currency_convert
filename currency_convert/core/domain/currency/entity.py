import datetime
import typing

from currency_convert.core.domain.currency.code import CurrencyCode
from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin


class Currency(Entity, DateTimeMixin):
    code: CurrencyCode
    name: str

    @classmethod
    def create(
        cls,
        code: str,
        name: str,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> typing.Self:
        value = CurrencyCode.create(code)
        return cls(
            code=value,
            name=name,
            created_at=created_at,
            updated_at=updated_at,
        )

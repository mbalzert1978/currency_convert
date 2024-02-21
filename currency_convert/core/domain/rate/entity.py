import datetime
import decimal
import typing

import pydantic

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin
from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.money import Money


class Rate(Entity, DateTimeMixin):
    rate: Money

    @classmethod
    def create(
        cls,
        rate: decimal.Decimal,
        created_at: datetime.datetime | None = None,
        updated_at: datetime.datetime | None = None,
    ) -> Result[typing.Self, pydantic.ValidationError]:
        if (mc_result := Money.create(rate)).is_failure():
            return Result.from_failure(mc_result)
        return Result.from_value(
            cls(
                rate=mc_result.unwrap(),
                created_at=created_at,
                updated_at=updated_at,
            )
        )

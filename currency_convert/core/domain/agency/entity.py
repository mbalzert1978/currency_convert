import datetime
import typing

import pydantic

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin
from currency_convert.core.domain.shared.result.result import Result
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
    ) -> Result[typing.Self, pydantic.ValidationError]:
        if (cc_result := CurrencyCode.create(code)).is_failure():
            return Result.from_failure(cc_result)
        return Result.from_value(
            cls(
                base_currency=cc_result.unwrap(),
                created_at=created_at,
                updated_at=updated_at,
            )
        )

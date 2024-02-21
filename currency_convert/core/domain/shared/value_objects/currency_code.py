import typing

import pydantic

from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.value_object import (
    ValueObject,
)

CODE_LEN = 3
DEFAULT = "EUR"


class CurrencyCode(ValueObject[str]):
    value: str = pydantic.Field(min_length=CODE_LEN, max_length=CODE_LEN)

    @classmethod
    def create(
        cls, value: str = DEFAULT
    ) -> Result[typing.Self, pydantic.ValidationError]:
        try:
            return Result.from_value(cls(value=value))
        except pydantic.ValidationError as e:
            return Result.from_failure(e)

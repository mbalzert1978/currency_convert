import decimal
import typing

import pydantic

from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.value_objects.value_object import ValueObject

PRECISION = decimal.Decimal(10) ** -8
DEFAULT = decimal.Decimal(0)
_DecimalNew: typing.TypeAlias = decimal.Decimal | float | str | tuple[int, typing.Sequence[int], int]


class Money(ValueObject[decimal.Decimal]):
    value: _DecimalNew  # type: ignore[assignment]

    @pydantic.field_validator("value", mode="after")
    @classmethod
    def quantize(cls, value: _DecimalNew) -> decimal.Decimal:
        try:
            return decimal.Decimal(value).quantize(PRECISION).copy_abs()
        except decimal.InvalidOperation as exc:
            raise ValueError(strings_error.INVALID_VALUE % value) from exc

    @classmethod
    def create(cls, value: _DecimalNew = DEFAULT) -> typing.Self:
        return cls(value=value)

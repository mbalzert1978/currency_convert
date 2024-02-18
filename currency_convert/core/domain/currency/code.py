import typing

import pydantic

from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.value_object import ValueObject

CODE_LEN = 3


class CurrencyCode(ValueObject[str]):
    value: str

    @pydantic.field_validator("value")
    @classmethod
    def validate_(cls, value: str) -> str:
        if value is None or len(value) != CODE_LEN:
            raise ValueError(strings_error.INVALID_VALUE % value)
        return value

    @classmethod
    def create(cls, value: str) -> typing.Self:
        return cls(value=value)

from __future__ import annotations

import dataclasses
import typing

from currency_convert.domain.primitives.valueobject import ValueObject, ValueObjectError

T = typing.TypeVar("T")


class InvalidCurrencyError(ValueObjectError):
    """Error raised when an invalid currency is provided."""


@dataclasses.dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class Currency(ValueObject[str]):
    VALID_LENGTH: typing.ClassVar[int] = 3
    ERROR_MSG: typing.ClassVar[str] = (
        f"Currency code must be {VALID_LENGTH} characters long. Got: {{code}}"
    )

    code: str

    def __eq__(self, other: T) -> bool:
        return isinstance(other, (str, Currency)) and self.code == other

    @classmethod
    def from_str(cls, value: str) -> typing.Self:
        if cls.has_valid_length(value) and value.isalpha():
            return cls(code=value)
        raise InvalidCurrencyError(cls.ERROR_MSG.format(code=value))

    @classmethod
    def has_valid_length(cls, code: typing.Sized) -> bool:
        return len(code) == cls.VALID_LENGTH

    def get_values(self) -> typing.Iterator[str]:
        yield self.code

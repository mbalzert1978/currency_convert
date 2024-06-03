from __future__ import annotations

import dataclasses
import typing

from results import Result

from currency_convert.domain.primitives.valueobject import ValueObject, ValueObjectError

T = typing.TypeVar("T")


class CurrencyError(ValueObjectError):
    """Base class for errors related to Currency."""


class InvalidCurrencyError(CurrencyError):
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
    def create(cls, code: str) -> Result[typing.Self, InvalidCurrencyError]:
        if cls.has_valid_length(code):
            return Result.Ok(cls(code=code))
        return Result.Err(InvalidCurrencyError(cls.ERROR_MSG.format(code=code)))

    @classmethod
    def has_valid_length(cls, code: typing.Sized) -> bool:
        return len(code) == cls.VALID_LENGTH

    def get_values(self) -> typing.Iterator[str]:
        yield self.code

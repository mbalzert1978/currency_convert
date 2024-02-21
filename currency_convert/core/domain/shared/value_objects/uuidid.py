from __future__ import annotations

import typing
import uuid

import pydantic

from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.value_object import (
    ValueObject,
)

TV = typing.TypeVar("TV", bound=typing.Any)
DEFAULT_FN = uuid.uuid4


class UUIDID(ValueObject[TV | uuid.UUID]):
    value: TV | uuid.UUID

    @typing.overload
    @classmethod
    def create(cls, value: TV) -> Result[UUIDID[TV], pydantic.ValidationError]:
        ...

    @typing.overload
    @classmethod
    def create(cls) -> Result[UUIDID[uuid.UUID], pydantic.ValidationError]:
        ...

    @classmethod
    def create(
        cls, value: TV | None = None
    ) -> Result[UUIDID[uuid.UUID] | UUIDID[TV], pydantic.ValidationError]:
        try:
            return Result.from_value(cls(value=value or DEFAULT_FN()))
        except pydantic.ValidationError as exc:
            return Result.from_failure(exc)

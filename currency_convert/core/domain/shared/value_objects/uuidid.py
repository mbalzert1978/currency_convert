from __future__ import annotations

import typing
import uuid

from currency_convert.core.domain.shared.value_objects.value_object import (
    ValueObject,
)

TV = typing.TypeVar("TV", bound=typing.Any)
DEFAULT_FN = uuid.uuid4


class UUIDID(ValueObject[TV | uuid.UUID]):
    value: TV | uuid.UUID

    @typing.overload
    @classmethod
    def create(cls, value: TV) -> UUIDID[TV]:
        ...

    @typing.overload
    @classmethod
    def create(cls) -> UUIDID[uuid.UUID]:
        ...

    @classmethod
    def create(cls, value: TV | None = None) -> UUIDID[uuid.UUID] | UUIDID[TV]:
        return cls(value=value or DEFAULT_FN())

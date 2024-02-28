from __future__ import annotations

import datetime
import functools
import typing

import pydantic
import pydantic.functional_validators as pfv

from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID

UTC_NOW = functools.partial(datetime.datetime.now, datetime.timezone.utc)


def _set_datetime_with_timezone(value: datetime.datetime | None) -> datetime.datetime:
    match value:
        case None:
            value = UTC_NOW()
        case datetime.datetime() if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        case _:
            raise ValueError(strings_error.INVALID_VALUE % value)
    return value


class ConfigMixin(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)


class CreatedAtMixin(pydantic.BaseModel):
    created_at: typing.Annotated[datetime.datetime | None, pfv.BeforeValidator(_set_datetime_with_timezone)]


class UpdatedAtMixin(pydantic.BaseModel):
    updated_at: typing.Annotated[datetime.datetime | None, pfv.BeforeValidator(_set_datetime_with_timezone)]


class TimestampMixin(pydantic.BaseModel):
    timestamp: datetime.datetime = pydantic.Field(default_factory=UTC_NOW)


class IDMixin(pydantic.BaseModel):
    id_: UUIDID = pydantic.Field(default_factory=UUIDID.create)

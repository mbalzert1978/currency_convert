from __future__ import annotations

import datetime
import functools

import pydantic

from currency_convert.core.domain.resources import strings_error

UTC_NOW = functools.partial(datetime.datetime.now, datetime.timezone.utc)


class DateTimeMixin(pydantic.BaseModel):
    created_at: datetime.datetime = pydantic.Field(default_factory=UTC_NOW)
    updated_at: datetime.datetime = pydantic.Field(default_factory=UTC_NOW)

    @pydantic.field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def validate_(cls, value: datetime.datetime) -> datetime.datetime:
        if not isinstance(value, datetime.datetime):
            raise TypeError(strings_error.INVALID_VALUE % value)
        if value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value

from __future__ import annotations

import datetime
import functools

import pydantic

from currency_convert.core.domain.resources import strings_error

UTC_NOW = functools.partial(datetime.datetime.now, datetime.timezone.utc)


class DateTimeMixin(pydantic.BaseModel):
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    @pydantic.field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def validate_(cls, value: datetime.datetime | None) -> datetime.datetime:
        match value:
            case None:
                value = UTC_NOW()
            case datetime.datetime() if value.tzinfo is None:
                value = value.replace(tzinfo=datetime.timezone.utc)
            case _:
                raise ValueError(strings_error.INVALID_VALUE % value)
        return value

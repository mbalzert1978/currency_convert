from __future__ import annotations

import uuid

import pydantic


class UUIDID(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(frozen=True)
    value: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)

    @classmethod
    def create(cls: type[UUIDID], value: uuid.UUID) -> UUIDID:
        return cls(value=value)

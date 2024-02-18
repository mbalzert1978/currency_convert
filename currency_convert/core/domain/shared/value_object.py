import typing

import pydantic

TV = typing.TypeVar("TV")


class ValueObject(pydantic.BaseModel, typing.Generic[TV]):
    model_config = pydantic.ConfigDict(frozen=True)
    value: TV

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.value == __value.value
        return False

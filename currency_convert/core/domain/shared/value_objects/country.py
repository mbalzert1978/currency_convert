import typing

from currency_convert.core.domain.shared.value_objects.value_object import ValueObject

DEFAULT = "Brussels"


class Country(ValueObject[str]):
    value: str

    @classmethod
    def create(cls, value: str = DEFAULT) -> typing.Self:
        return cls(value=value)

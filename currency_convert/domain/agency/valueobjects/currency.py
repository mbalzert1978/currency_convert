import dataclasses
import typing

from currency_convert.domain.primitives.valueobject import ValueObject

T = typing.TypeVar('T')

@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Currency(ValueObject[str]):
    code: str

    def get_atomic_values(self) -> typing.Iterator[str]:
        yield self.code
import dataclasses
from typing import Sequence, TypeVar
import abc

T = TypeVar("T")


@dataclasses.dataclass(frozen=True, slots=True)
class ValueObject(abc.ABC):
    @abc.abstractmethod
    def get_attomic_values(self) -> Sequence[T]:
        raise NotImplementedError

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, type(self))
            and self.get_attomic_values() == value.get_attomic_values()
        )

    def __hash__(self) -> int:
        return hash(self.get_attomic_values()) * 41

import dataclasses
import abc
import typing

T = typing.TypeVar("T")


@dataclasses.dataclass(frozen=True, slots=True)
class ValueObject(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def get_atomic_values(self) -> typing.Iterator[T]:
        raise NotImplementedError

    def __eq__(self, value: object) -> bool:
        return (
            isinstance(value, type(self))
            and self.get_atomic_values() == value.get_atomic_values()
        )

    def __hash__(self) -> int:
        return hash(self.get_atomic_values()) * 41

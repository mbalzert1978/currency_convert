from __future__ import annotations

import abc
import dataclasses
import typing

T = typing.TypeVar("T")


@dataclasses.dataclass(frozen=True, slots=True)
class ValueObject(abc.ABC, typing.Generic[T]):
    @abc.abstractmethod
    def get_atomic_values(self) -> typing.Iterator[T]:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self._equals(other)

    def _equals(self, other: ValueObject[T]) -> bool:
        return all(
            self == other
            for self, other in zip(self.get_atomic_values(), other.get_atomic_values())
        )

    def __hash__(self) -> int:
        return hash(self.get_atomic_values()) * 41

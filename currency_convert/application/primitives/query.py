from __future__ import annotations
import dataclasses
import typing

from results import Result

T = typing.TypeVar("T")
E = typing.TypeVar("E")
Qcontra = typing.TypeVar("Qcontra", bound="Query", contravariant=True)


@dataclasses.dataclass(frozen=True)
class Query:
    pass


class QueryHandler(typing.Protocol[Qcontra, T, E]):
    def execute(self, query: Qcontra) -> Result[T, E]: ...

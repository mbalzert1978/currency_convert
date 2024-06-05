from __future__ import annotations

import dataclasses
import typing

Tco = typing.TypeVar("Tco", covariant=True)
Qcontra = typing.TypeVar("Qcontra", bound="Query", contravariant=True)


@dataclasses.dataclass(frozen=True)
class Query:
    pass


class QueryHandler(typing.Protocol[Tco, Qcontra]):
    def execute(self, query: Qcontra) -> Tco: ...

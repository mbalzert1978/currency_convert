import typing

from currency_convert.core.domain.shared.query import Query
from currency_convert.core.domain.shared.result.result import Result

_TQ_contra = typing.TypeVar("_TQ_contra", bound=Query, contravariant=True)
_RV_co = typing.TypeVar("_RV_co", bound=Result, covariant=True)  # type:ignore[type-arg]


class QueryHandler(typing.Protocol[_TQ_contra, _RV_co]):
    def handle(self, cmd: _TQ_contra) -> _RV_co: ...

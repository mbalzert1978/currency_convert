import types
import typing

from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.returns import Result


_TK = typing.TypeVar("_TK")
_TV = typing.TypeVar("_TV")


class QueryAdapter(typing.Protocol):
    def __enter__(self) -> typing.Self: ...


    def __exit__(
        self,
        __exc_type: type[BaseException] | None = None,
        __exc_value: BaseException | None = None,
        __traceback: types.TracebackType | None = None,
    ) -> None: ...

    def execute(
        self, query: str, parameter: dict[_TV, _TK]
    ) -> Result[tuple[typing.Any, ...], Error]: ...

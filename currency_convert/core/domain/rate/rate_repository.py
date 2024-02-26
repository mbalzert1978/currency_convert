import types
import typing

from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result


class IRateRepository(typing.Protocol):
    def __enter__(self) -> typing.Self:
        ...

    def __exit__(
        self,
        __exc_type: type[BaseException] | None = None,
        __exc_value: BaseException | None = None,
        __traceback: types.TracebackType | None = None,
    ) -> None:
        ...

    def add(self, rate: Rate) -> Result[None, Error]:
        ...

    def add_many(self, rates: typing.Sequence[Rate]) -> Result[None, Error]:
        ...

import types
import typing

from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result


class IAgencyRepository(typing.Protocol):
    def __enter__(self) -> typing.Self:
        ...

    def __exit__(
        self,
        __exc_type: typing.Optional[type[BaseException]],
        __exc_value: typing.Optional[BaseException],
        __traceback: typing.Optional[types.TracebackType],
    ) -> Result[typing.Optional[bool], Error]:
        ...

    def find_by_name(self, name: str) -> Result[typing.Optional[Agency], Error]:
        ...

    def add(self, agency: Agency) -> Result[None, Error]:
        ...

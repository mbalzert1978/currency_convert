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
        __exc_type: type[BaseException] | None = None,
        __exc_value: BaseException | None = None,
        __traceback: types.TracebackType | None = None,
    ) -> Result[bool | None, Error]:
        ...

    def find_by_name(self, name: str) -> Result[Agency | None, Error]:
        ...

    def add(self, agency: Agency) -> Result[None, Error]:
        ...

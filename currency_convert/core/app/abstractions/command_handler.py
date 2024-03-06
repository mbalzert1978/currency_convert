import typing

from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.result.result import Result

_TC_contra = typing.TypeVar("_TC_contra", bound=Command, contravariant=True)
_RV_co = typing.TypeVar("_RV_co", bound=Result, covariant=True)  # type:ignore[type-arg]


class CommandHandler(typing.Protocol[_TC_contra, _RV_co]):
    def handle(self, cmd: _TC_contra) -> _RV_co: ...

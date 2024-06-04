import dataclasses
import typing

from results import Result

T = typing.TypeVar("T")
E = typing.TypeVar("E")


@dataclasses.dataclass(frozen=True)
class Command:
    pass


class CommandHandler(typing.Protocol[T, E]):
    def execute(self, q: Command) -> Result[T, E]: ...

import dataclasses
import typing

Tco = typing.TypeVar("Tco", covariant=True)
Ccontra = typing.TypeVar("Ccontra", bound="Command", contravariant=True)


@dataclasses.dataclass(frozen=True)
class Command:
    pass


class CommandHandler(typing.Protocol[Ccontra, Tco]):
    def execute(self, q: Ccontra) -> Tco: ...

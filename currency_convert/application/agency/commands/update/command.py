import dataclasses

from currency_convert.application.primitives.command import Command
from currency_convert.domain.agency.entities.interface import UpdateStrategy


@dataclasses.dataclass(frozen=True)
class Update(Command):
    strategy: UpdateStrategy


@dataclasses.dataclass(frozen=True)
class UpdatebyName(Update):
    name: str


@dataclasses.dataclass(frozen=True)
class UpdatebyId(Update):
    id: str

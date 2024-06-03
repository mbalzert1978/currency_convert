import dataclasses

from currency_convert.application.primitives.command import Command


@dataclasses.dataclass(frozen=True)
class CreateAgency(Command):
    name: str
    base: str
    address: str
    country: str

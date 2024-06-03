import dataclasses
import uuid

from currency_convert.domain.primitives.error import ConverterError


class EntityError(ConverterError):
    """Base class for errors related to Entities."""


@dataclasses.dataclass(slots=True)
class Entity:
    id: uuid.UUID

    def __eq__(self, value: object) -> bool:
        return isinstance(value, type(self)) and self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id) * 41


@dataclasses.dataclass(slots=True, eq=False)
class AggregateRoot(Entity):
    pass

import dataclasses
import uuid


@dataclasses.dataclass(slots=True)
class Entity:
    id_: uuid.UUID

    def __eq__(self, value: object) -> bool:
        return isinstance(value, type(self)) and self.id_ == value.id_

    def __hash__(self) -> int:
        return hash(self.id_) * 41


@dataclasses.dataclass(slots=True, eq=False)
class AggregateRoot(Entity):
    pass
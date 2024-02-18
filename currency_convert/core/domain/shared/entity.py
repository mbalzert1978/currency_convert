import abc
import typing

import pydantic

from currency_convert.core.domain.shared.domain_event import DomainEvent
from currency_convert.core.domain.shared.mixin import IDMixin

TV = typing.TypeVar("TV")


class Entity(IDMixin, abc.ABC):
    domain_events: list[DomainEvent] = pydantic.Field(
        default_factory=list,
        init=False,
    )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.id_.value == __value.id_.value
        return False

    def send(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)

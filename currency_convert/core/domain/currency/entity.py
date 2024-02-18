import typing

from currency_convert.core.domain.currency.code import CurrencyCode
from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import DateTimeMixin


class Currency(Entity, DateTimeMixin):
    code: CurrencyCode
    name: str

    @classmethod
    def create(cls, code: str, name: str) -> typing.Self:
        value = CurrencyCode.create(code)
        return cls(code=value, name=name)

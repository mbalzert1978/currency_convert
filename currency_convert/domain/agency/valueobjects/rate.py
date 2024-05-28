import dataclasses

from currency_convert.domain.agency.valueobjects.currency import Currency
from currency_convert.domain.agency.valueobjects.money import Money
from currency_convert.domain.primitives.valueobject import ValueObject


@dataclasses.dataclass(frozen=True, slots=True, eq=False)
class Rate(ValueObject[Currency]):
    currency_from: Currency
    currency_to: Currency
    rate: Money

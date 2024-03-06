from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money


class CreateRate(Command):
    agency_name: str
    to_currency: CurrencyCode
    rate: Money

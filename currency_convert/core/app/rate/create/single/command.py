from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.money import Money


class CreateRate(Command):
    agency_name: str
    base_currency: CurrencyCode
    to_currency: CurrencyCode
    rate: Money
    residing_coutry: Country

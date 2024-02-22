from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode


class UpdateAgency(Command):
    name: str
    base_currency: CurrencyCode | None = None
    residing_country: Country | None = None

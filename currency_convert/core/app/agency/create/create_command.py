import pydantic

from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode

CODE_LEN = 3


class CreateAgencyCommand(Command):
    name: str
    base_currency: CurrencyCode = pydantic.Field(min_length=CODE_LEN, max_length=CODE_LEN)
    residing_country: Country

import typing

from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class UpdateAgency(Command):
    id_: UUIDID[typing.Any]
    name: str | None = None
    base_currency: CurrencyCode | None = None
    residing_country: Country | None = None

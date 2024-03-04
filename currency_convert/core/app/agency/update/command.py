from currency_convert.core.domain.shared.command import Command
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class UpdateAgency(Command):
    id_: UUIDID  # type:ignore[type-arg]
    name: str | None = None
    base_currency: CurrencyCode | None = None
    residing_country: Country | None = None

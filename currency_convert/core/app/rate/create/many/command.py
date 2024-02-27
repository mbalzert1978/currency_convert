from collections.abc import Sequence

from currency_convert.core.domain.rate.entity import Rate
from currency_convert.core.domain.shared.command import Command


class CreateRates(Command):
    agency_name: str
    rates: Sequence[Rate]

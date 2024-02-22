import datetime
import typing

from currency_convert.core.domain.shared.entity import Entity
from currency_convert.core.domain.shared.mixin import CreatedAtMixin, UpdatedAtMixin
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class Agency(Entity, CreatedAtMixin, UpdatedAtMixin):
    name: str
    base_currency: CurrencyCode
    residing_country: Country

    @classmethod
    def create(
        cls,
        name: str,
        base_currency: CurrencyCode,
        residing_country: Country,
    ) -> typing.Self:
        return cls(
            name=name,
            base_currency=base_currency,
            residing_country=residing_country,
            created_at=None,
            updated_at=None,
        )

    @classmethod
    def update(  # noqa: PLR0913
        cls,
        id_: UUIDID,
        name: str,
        base_currency: CurrencyCode,
        residing_country: Country,
        created_at: datetime.datetime,
    ) -> typing.Self:
        return cls(
            id_=id_,
            name=name,
            base_currency=base_currency,
            residing_country=residing_country,
            created_at=created_at,
            updated_at=None,
        )

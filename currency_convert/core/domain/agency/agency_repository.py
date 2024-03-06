import types
import typing

from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.maybe import Maybe
from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class IAgencyRepository(typing.Protocol):
    def __enter__(self) -> typing.Self: ...

    def __exit__(
        self,
        __exc_type: type[BaseException] | None = None,
        __exc_value: BaseException | None = None,
        __traceback: types.TracebackType | None = None,
    ) -> None: ...

    def get(self, id_: UUIDID) -> Result[Maybe[Agency, None], Error]:  # type:ignore[type-arg]
        ...

    def find_by_name(self, name: str) -> Result[Maybe[Agency, None], Error]: ...

    def add(self, agency: Agency) -> Result[None, Error]: ...

    def update(
        self,
        agency: Agency,
        name: str | None = None,
        base_currency: CurrencyCode | None = None,
        residing_country: Country | None = None,
    ) -> Result[None, Error]: ...

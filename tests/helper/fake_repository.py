import types
import typing
from currency_convert.core.domain.shared.entity import Entity

from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.maybe import Maybe
from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.country import Country
from currency_convert.core.domain.shared.value_objects.currency_code import CurrencyCode
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID

ModelType = typing.TypeVar("ModelType", bound=Entity)


class FakeRepository(typing.Generic[ModelType]):
    def __init__(self, entities: set[ModelType] | None = None, raise_on: str | None = None) -> types.NoneType:
        self._raise_on = raise_on
        self._entities: set[ModelType] = entities or set()

    def __enter__(self) -> typing.Self:
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None = None,
        __exc_value: BaseException | None = None,
        __traceback: types.TracebackType | None = None,
    ) -> None:
        if __exc_value is not None:
            raise Error(500, "Unreachable", __exc_type, __traceback)

    def get(self, id_: UUIDID) -> Result[Maybe[ModelType, None], Error]:
        if self._raise_on is not None and self._raise_on in "get":
            return Result.from_failure(Error(500, "Test_error"))
        return self._getter(lambda e: e.id_ == id_)

    def find_by_name(self, name: str) -> Result[Maybe[ModelType, None], Error]:
        if self._raise_on is not None and self._raise_on in "find_by_name":
            return Result.from_failure(Error(500, "Test_error"))
        return self._getter(lambda e: e.name == name)

    def _getter(self, filter_fn: typing.Callable[[ModelType], bool]):
        try:
            found = next(entity for entity in self._entities if filter_fn(entity))
        except StopIteration:
            return Result.from_failure(Maybe.from_none(None))
        except Exception as exc:
            return Result.from_failure(Error(404, "Not found.", exc))
        else:
            return Result.from_value(Maybe.from_value(found))

    def add(self, entity: ModelType) -> Result[None, Error]:
        if self._raise_on is not None and self._raise_on in "add":
            return Result.from_failure(Error(500, "Test_error"))
        try:
            self._entities.add(entity)
        except Exception as exc:
            return Result.from_failure(Error(500, "Internal Error", exc))
        else:
            return Result.from_value(None)

    def update(
        self,
        entity: ModelType,
        name: str | None = None,
        base_currency: CurrencyCode | None = None,
        residing_country: Country | None = None,
    ) -> Result[None, Error]:
        if self._raise_on is not None and self._raise_on in "update":
            return Result.from_failure(Error(500, "Test_error"))
        entity.name = name or entity.name
        entity.base_currency = base_currency or entity.base_currency
        entity.residing_country = residing_country or entity.residing_country
        return self.add(entity)

    def add_many(self, entities: typing.Sequence[ModelType]) -> Result[None, Error]:
        if self._raise_on is not None and self._raise_on in "add_many":
            return Result.from_failure(Error(500, "Test_error"))
        for entity in entities:
            res = self.add(entity)
            if res.is_failure():
                return res
        return res

    def _get_first_entity(self) -> ModelType:
        return next(iter(self._entities))

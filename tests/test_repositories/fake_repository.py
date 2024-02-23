import types
import typing
from currency_convert.core.domain.shared.entity import Entity

from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID

ModelType = typing.TypeVar("ModelType", bound=Entity)


class FakeRepository(typing.Generic[ModelType]):
    def __init__(self) -> types.NoneType:
        self._entities: set[ModelType] = set()

    def __enter__(self) -> typing.Self:
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None = None,
        __exc_value: BaseException | None = None,
        __traceback: types.TracebackType | None = None,
    ) -> Result[bool | None, Error]:
        if __exc_value is not None:
            return Result.from_failure(Error(500, "Internal Error", __exc_type, __traceback))
        return Result.from_value(None)

    def find_by_name(self, name: str) -> Result[ModelType | None, Error]:
        found = next((entity for entity in self._entities if entity.name == name), None)
        if found is None:
            return Result.from_failure(Error(404, "Not found."))
        return Result.from_value(found)

    def add(self, entity: ModelType) -> Result[None, Error]:
        try:
            self._entities.add(entity)
        except Exception as exc:
            return Result.from_failure(exc)
        else:
            return Result.from_value(None)

    def update(self, entity: ModelType) -> Result[None, Error]:
        return self.add(entity)

    def add_many(self, entities: typing.Sequence[ModelType]) -> Result[None, Error]:
        for entity in entities:
            res = self.add(entity)
            if res.is_failure():
                return res
        return res

    def _get_first_entity(self) -> ModelType | None:
        return next(iter(self._entities), None)

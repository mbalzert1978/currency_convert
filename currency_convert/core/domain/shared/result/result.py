import typing

from currency_convert.core.domain.shared.error import CurrencyConverterError

_T = typing.TypeVar("_T")
_E = typing.TypeVar("_E")
_T_new = typing.TypeVar("_T_new")


class UnwrapFailedError(CurrencyConverterError):
    """Unwrap failed error."""


@typing.runtime_checkable
class Result(typing.Protocol[_T, _E]):
    __slots__ = ("_inner_value",)

    _inner_value: _T | _E

    def __init__(self, inner_value: _T | _E) -> None:
        self._inner_value = inner_value

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, type(self)) and self._inner_value == __value._inner_value

    def __ne__(self, __value: object) -> bool:
        return not (self == __value)

    def value_or(
        self,
        default_value: _T_new,
    ) -> _T | _T_new:
        """
        Get value or default value.

        .. code:: python
        >>> assert Success(1).value_or(2) == 1
        ... assert Failure(1).value_or(2) == 2

        """

    def unwrap(self) -> _T:
        """
        Get value or raise exception.

        .. code:: python
        >>> assert Success(1).unwrap() == 1

        ... Failure(1).unwrap()
        Traceback (most recent call last):
        ...
        returns.UnwrapFailedError

        """

    def failure(self) -> _E:
        """
        Get failed value or raise exception.

        .. code:: python
        >>> assert Failure(1).failure() == 1

        ... Success(1).failure()
            Traceback (most recent call last):
            ...
            returns.UnwrapFailedError

        """

    @classmethod
    def from_value(
        cls,
        inner_value: _T_new,
    ) -> "Result[_T_new, typing.Any]":
        """
        One more value to create success unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python
        >>> assert Result.from_value(1) == Success(1)

        You can use this method or :func:`~Success`,
        choose the most convenient for you.

        """
        return Success(inner_value)

    @classmethod
    def from_failure(cls, inner_value: _E) -> "Result[typing.Any, _E]":
        """
        One more value to create failure unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python
        >>> assert Result.from_failure(1) == Failure(1)

        You can use this method or :func:`Failure`,
        choose the most convenient for you.

        """
        return Failure(inner_value)

    def is_success(self) -> bool:
        """
        Check if the operation represented by this instance is successful.

        .. code:: python
        >>> assert Result.from_value(1).is_success()
        """

    def is_failure(self) -> bool:
        """
        Check if the operation represented by this instance is a failure.

        .. code:: python
        >>> assert Result.from_failure(Exception()).is_failure()
        """

    def bind(self, function: typing.Callable[[_T], "Result[_T, _E]"]) -> "Result[_T, _E]":
        """
        Binds the current result to a function returning another result.
        Use this when the function intodruces side effects.

        .. code:: python
        >>> result = Result.from_success(10)
        ...
        ...
        ... def factory(inner_value: int) -> Result[int, str]:
        ...     if inner_value > 0:
        ...         return Result.from_value(inner_value * 2)
        ...     return Result.from_failure(str(inner_value))
        ...
        ...
        ... assert result.bind(factory) == Result.from_success(20)
        """

    def map(self, function: typing.Callable[[_T], _T_new]) -> "Result[_T_new, _E]":
        """
        Maps the current result to a new value using a function.
        Use this when the function doesn't introduce side effects

        .. code:: python
        >>> result = Result.from_success(10)
        ... assert result.map(bool) == Result.from_success(True)
        """


@typing.final
class Success(Result[_T, typing.Any]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[_T]:
        yield self._inner_value

    def __repr__(self) -> str:
        return f"Success({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((True, self._inner_value))

    def __init__(self, inner_value: _T) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> _T:
        return self._inner_value

    def value_or(self, _: _T_new) -> _T:
        return self._inner_value

    def failure(self) -> typing.NoReturn:
        raise UnwrapFailedError(self)

    def is_success(self) -> typing.Literal[True]:
        return True

    def is_failure(self) -> typing.Literal[False]:
        return False

    def bind(self, function: typing.Callable[[_T], Result[_T, _E]]) -> Result[_T, _E]:
        return function(self._inner_value)

    def map(self, function: typing.Callable[[_T], _T_new]) -> Result[_T_new, _E]:
        return Result.from_value(function(self._inner_value))


@typing.final
class Failure(Result[typing.Any, _E]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[typing.NoReturn]:
        def _iter() -> typing.Iterator[typing.NoReturn]:
            # Exception will be raised when the iterator is advanced, not when it's created
            raise UnwrapFailedError(self)
            yield  # This yield will never be reached, but is necessary to create a generator

        return _iter()

    def __repr__(self) -> str:
        return f"Failure({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((False, self._inner_value))

    def __init__(self, inner_value: _E) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> typing.NoReturn:
        match self._inner_value:
            case Exception():
                raise self._inner_value
            case _:
                raise UnwrapFailedError(self)

    def value_or(self, default_value: _T_new) -> _T_new:
        return default_value

    def failure(self) -> _E:
        return self._inner_value

    def is_success(self) -> typing.Literal[False]:
        return False

    def is_failure(self) -> typing.Literal[True]:
        return True

    def bind(self, _: typing.Callable[[_T], Result[_T, _E]]) -> Result[_T, _E]:
        return self

    def map(self, _: typing.Callable[[_T], _T_new]) -> Result[_T_new, _E]:
        return self

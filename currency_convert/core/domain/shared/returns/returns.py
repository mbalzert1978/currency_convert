from __future__ import annotations

import typing

from currency_convert.core.domain.shared.error import CurrencyConverterError

_T = typing.TypeVar("_T")
_E = typing.TypeVar("_E")
_T_new = typing.TypeVar("_T_new")


class UnwrapFailedError(CurrencyConverterError):
    """Unwrap failed error."""


@typing.runtime_checkable
class Result(typing.Protocol[_T, _E]):
    """Type `Result` represents a result: every `Result` is either `Success`,
    containing a value, or `Failure`, containing an error.
    """

    __slots__ = ("_inner_value",)

    _inner_value: _T | _E

    @classmethod
    def from_value(
        cls,
        inner_value: _T_new,
    ) -> Result[_T_new, typing.Any]:
        return Success(inner_value)

    @classmethod
    def from_failure(cls, inner_value: _E) -> Result[typing.Any, _E]:
        return Failure(inner_value)

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, type(self))
            and self._inner_value == __value._inner_value
        )

    def __ne__(self, __value: object) -> bool:
        return not (self == __value)

    def unwrap(self) -> _T:
        """Get value or raise exception.
        .. code:: python
        >>> assert Result.from_value(1).unwrap() == 1
        >>> assert Result.from_failure(1).unwrap()
         Traceback (most recent call last): raise UnwrapFailedError(self)
        """

    def value_or(
        self,
        default_value: _T_new,
    ) -> _T | _T_new:
        """Get value or default value.
        .. code:: python
        >>> assert Result.from_value(1).value_or(2) == 1
        >>> assert Result.from_failure(1).value_or(2) == 2

        """

    def failure(self) -> _E:
        """Get failed value or raise exception.
        .. code:: python
        >>> assert Result.from_failure(1).failure() == 1
        >>> assert Result.from_value(1).failure()
         Traceback (most recent call last): raise UnwrapFailedError(self)
        """

    def is_success(self) -> bool:
        """Check if the operation represented by this instance is successful.
        .. code:: python
        >>> assert Result.from_value(1).is_success()
        >>> assert not Result.from_failure(1).is_success()
        """

    def is_failure(self) -> bool:
        """Check if the operation represented by this instance is a failure.
        .. code:: python
        >>> assert Result.from_failure(1).is_failure()
        >>> assert not Result.from_value(1).is_failure()
        """

    def ok(self) -> Option[_T]:
        """Converts from `Result<_T, E>` to [`Option<_T>`].
        .. code:: python
        >>> assert Result.from_value(1).ok() == Option.from_value(1)
        >>> assert Result.from_failure(1).ok() == Option.from_none(1)
        """

    def bind(self, function: typing.Callable[[_T], Result[_T, _E]]) -> Result[_T, _E]:
        """
        Maps an Result<_T>s contained value to a function that returns an Result<_T>.
        .. code:: python
        >>> def parse(f: str) -> Result[int, ValueError]:
        ...     try:
        ...         return Result.from_value(int(f))
        ...    except ValueError as exc:
        ...         return Result.from_failure(exc)
        >>> assert Result.from_value("10").bind(parse) == Result.from_value(10)
         Traceback (most recent call last): raise ValueError
        """

    def map(self, function: typing.Callable[[_T], _T_new]) -> Result[_T_new, _E]:
        """
        Maps an Result<_T> to Result<_T_new>
         by applying a function (no sideeffects) to a contained value or returns Failure.
        .. code:: python
        >>> assert Result.from_value(10).map(bool) == Result.from_value(True)
        >>> assert Result.from_failure(10).map(bool) == Result.from_failure(10)
        """

    def map_or(
        self, default: _T_new, function: typing.Callable[[_T], _T_new]
    ) -> _T_new:
        """
        Computes a default function result,
         or applies a different function to the contained value.
        .. code:: python
        >>> assert Result.from_value("foo").map_or(42, len) == 3
        >>> assert Result.from_failure("bar").map_or(42, len) == 42
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
        self._inner_value = inner_value

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

    def ok(self) -> Option[_T]:
        return Option.from_value(self._inner_value)

    def bind(self, function: typing.Callable[[_T], Result[_T, _E]]) -> Result[_T, _E]:
        return function(self._inner_value)

    def map(self, function: typing.Callable[[_T], _T_new]) -> Result[_T_new, _E]:
        return Result.from_value(function(self._inner_value))

    def map_or(
        self,
        default: _T_new,
        function: typing.Callable[[_T], _T_new],
    ) -> _T_new:
        return function(self._inner_value)


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
        self._inner_value = inner_value

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

    def ok(self) -> Option[_T]:
        return Option.from_none(typing.cast(_T, self._inner_value))

    def bind(self, _: typing.Callable[[_T], Result[_T, _E]]) -> Result[_T, _E]:
        return self

    def map(self, _: typing.Callable[[_T], _T_new]) -> Result[_T_new, _E]:
        return self

    def map_or(
        self,
        default: _T_new,
        function: typing.Callable[[_T], _T_new],
    ) -> _T_new:
        return default


@typing.runtime_checkable
class Option(typing.Protocol[_T]):
    """Type `Option` represents an optional value: every `Option` is either `Some`,
    containing a value, or `Null`, representing the absence of a value."""

    __slots__ = ("_inner_value",)
    _inner_value: typing.Optional[_T]

    @classmethod
    def from_value(cls, value: _T) -> Option[_T]:
        return Some(value)

    @classmethod
    def from_none(cls, value: _T) -> Option[_T]:
        return Null(value)

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, type(self))
            and self._inner_value == __value._inner_value
        )

    def __ne__(self, __value: object) -> bool:
        return not (self == __value)

    def unwrap(self) -> typing.Optional[_T]:
        """Get value or None.
        .. code:: python
        >>> assert Option.from_value(1).unwrap() == 1
        >>> assert Option.from_none(1).unwrap() is None
        """

    def value_or(self, value: _T_new) -> _T | _T_new:
        """Get value or default value.
        .. code:: python
        >>> assert Option.from_value(1).is_some()
        >>> assert not Option.from_none(1).is_some()
        """

    def is_some(self) -> bool:
        """Check if the operation represented by this instance is Someful.
        .. code:: python
        >>> assert Option.from_value(1).is_some()
        >>> assert not Option.from_none(1).is_some()
        """

    def is_none(self) -> bool:
        """Check if the operation represented by this instance is a Null.
        .. code:: python
        >>> assert not Option.from_value(1).is_none()
        >>> assert Option.from_none(1).is_none()
        """

    def ok_or_else(self, err: _E) -> Result[_T, _E]:
        """
        Transforms the Option<_T> into a Result<_T, _E>,
         mapping Some(v) to Success(v) and None to Failure(err()).
        .. code:: python
        >>> assert Option.from_value(1).ok_or_else("Foo") == Result.from_value(1)
        >>> assert Option.from_none(1).ok_or_else("Foo") == Result.from_failure("Foo")
        """

    def bind(self, function: typing.Callable[[_T], Option[_T]]) -> Option[_T]:
        """
        Maps an Option<_T>s contained value to a function that returns an Option<_T>.
        .. code:: python
        >>> def mul_two(f: typing.Optional[int]) -> Option[int]:
        ...     return Null(f) if f is None else Some(f * 2)
        >>> assert Option.from_value(10).bind(mul_two) == Option.from_value(20)
        >>> assert Option.from_none(-10).bind(mul_two) == Option.from_none(None)
        """

    def map(self, function: typing.Callable[[_T], _T_new]) -> Option[_T_new | None]:
        """
        Maps an Option<_T> to Option<_T_new>
         by applying a function (no sideeffects) to a contained value or returns Null.
        .. code:: python
        >>> assert Option.from_value(10).map(bool) == Option.from_value(True)
        >>> assert Option.from_none(10).map(bool) == Option.from_none(None)
        """

    def map_or(
        self,
        default: _T_new,
        function: typing.Callable[[_T], _T_new],
    ) -> _T_new:
        """
        Computes a default function result,
         or applies a different function to the contained value.
        .. code:: python
        >>> assert Option.from_value("foo").map_or(42, len) == 3
        >>> assert Option.from_none("bar").map_or(42, len) == 42
        """


@typing.final
class Some(typing.Generic[_T], Option[_T]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[_T]:
        yield typing.cast(_T, self._inner_value)

    def __repr__(self) -> str:
        return f"Some({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((True, self._inner_value))

    def __init__(self, inner_value: _T) -> None:
        if inner_value is None:
            raise ValueError(f"Value {inner_value!r} is not allowed on Some.")
        self._inner_value = inner_value

    def unwrap(self) -> _T:
        return self._inner_value

    def value_or(self, _: _T_new) -> _T:
        return self._inner_value

    def is_some(self) -> typing.Literal[True]:
        return True

    def is_none(self) -> typing.Literal[False]:
        return False

    def ok_or_else(self, _: _E) -> Result[_T, _E]:
        return Result.from_value(self._inner_value)

    def bind(self, function: typing.Callable[[_T], Option[_T]]) -> Option[_T]:
        return function(self._inner_value)

    def map(self, function: typing.Callable[[_T], _T_new]) -> Option[_T_new]:
        return Some(function(self._inner_value))

    def map_or(
        self,
        default: _T_new,
        function: typing.Callable[[_T], _T_new],
    ) -> _T_new:
        return function(self._inner_value)


@typing.final
class Null(typing.Generic[_T], Option[_T]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[None]:
        yield None

    def __repr__(self) -> str:
        return f"Null({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((False, self._inner_value))

    def __init__(self, inner_value: _T) -> None:
        self._inner_value = None

    def unwrap(self) -> None:
        return self._inner_value

    def value_or(self, default_value: _T_new) -> _T_new:
        return default_value

    def is_some(self) -> typing.Literal[False]:
        return False

    def is_none(self) -> typing.Literal[True]:
        return True

    def ok_or_else(self, err: _E) -> Result[_T, _E]:
        return Result.from_failure(err)

    def bind(self, _: typing.Callable[[_T], Option[_T]]) -> Option[_T]:
        return self

    def map(self, _: typing.Callable[[_T], _T_new]) -> Option[_T_new]:
        return typing.cast(Option[_T_new], self)

    def map_or(
        self,
        default: _T_new,
        function: typing.Callable[[_T], _T_new],
    ) -> _T_new:
        return default

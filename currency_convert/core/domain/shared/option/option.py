from __future__ import annotations

import typing

from currency_convert.core.domain.shared.result.result import Result

_T = typing.TypeVar("_T")
_E = typing.TypeVar("_E")
_T_new = typing.TypeVar("_T_new")


@typing.runtime_checkable
class Option(typing.Protocol[_T]):
    """Type Option represents an optional value:
    every Option is either `Some` and contains a value, or `Null`, and does not."""

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

from __future__ import annotations

import typing

from currency_convert.core.domain.shared.result.result import Result

_T = typing.TypeVar("_T")
_E = typing.TypeVar("_E")
_T_new = typing.TypeVar("_T_new")


class EQMixin(typing.Generic[_T]):
    __slots__ = ("_inner_value",)
    _inner_value: typing.Optional[_T]

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, type(self))
            and self._inner_value == __value._inner_value
        )

    def __ne__(self, __value: object) -> bool:
        return not (self == __value)


@typing.final
class Some(typing.Generic[_T], EQMixin[_T]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[_T]:
        yield typing.cast(_T, self._inner_value)

    def __repr__(self) -> str:
        return f"Some({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((True, self._inner_value))

    def __init__(self, inner_value: _T) -> None:
        if inner_value is None or isinstance(inner_value, Exception):
            raise ValueError(f"Value {inner_value!r} is not allowed")
        self._inner_value = inner_value

    def unwrap(self) -> _T:
        """Get value or None.
        .. code:: python
        >>> assert Some(1).unwrap() == 1
        >>> assert Null(1).unwrap() is None
        """
        return typing.cast(_T, self._inner_value)

    def value_or(self, _: _T_new) -> _T:
        """Get value or default value.
        .. code:: python
        >>> assert Some(1).value_or(2) == 1
        >>> assert Null(1).value_or(2) == 2
        """
        return typing.cast(_T, self._inner_value)

    def is_some(self) -> typing.Literal[True]:
        """Check if the operation represented by this instance is Someful.
        .. code:: python
        >>> assert Some(1).is_some()
        """
        return True

    def is_none(self) -> typing.Literal[False]:
        """Check if the operation represented by this instance is a Null.
        .. code:: python
        >>> assert not Some(1).is_none()
        """
        return False

    def ok_or_else(self, _: _E) -> Result[_T, _E]:
        """
        Transforms the Option<_T> into a Result<_T, _E>,
         mapping Some(v) to Success(v) and None to Failure(err()).
        .. code:: python
        >>> assert Some(1).ok_or_else(Exception()) == Success(1)
        >>> assert Null(1).ok_or_else(Exception()) == Failure(Exception())
        """
        return Result.from_value(typing.cast(_T, self._inner_value))

    def bind(self, function: typing.Callable[[_T], Maybe[_T]]) -> Maybe[_T]:
        """
        Binds the current maybe to a function returning another maybe.
         Use this when the function intodruces side effects.
        .. code:: python
        >>> def factory(inner_value: int | None) -> Maybe[typing.Optional[int]]:
        ...     if inner_value > 0:
        ...         return Some(inner_value * 2)
        ...     return Null(inner_value)
        ...
        ... assert Some(10).bind(factory) == Some(20)
        ... assert Some(-10).bind(factory) == Null(None)
        """
        return function(typing.cast(_T, self._inner_value))

    def map(self, function: typing.Callable[[_T], _T_new]) -> Maybe[_T_new]:
        """
        Binds the current maybe to a function returning another maybe.
         Use this when the function intodruces no side effects.
        .. code:: python
        >>> assert Some(10).map(bool) == Some(True)
        ... assert Null(10).bind(bool) == Null(None)
        """
        return Some(function(typing.cast(_T, self._inner_value)))


@typing.final
class Null(typing.Generic[_T], EQMixin[_T]):
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
        """Get value or None.
        .. code:: python
        >>> assert Some(1).unwrap() == 1
        >>> Null(1).unwrap() is None
        """
        return None

    def value_or(self, default_value: _T_new) -> _T_new:
        """Get value or default value.
        .. code:: python
        >>> assert Some(1).value_or(2) == 1
        >>> assert Null(1).value_or(2) == 2
        """
        return default_value

    def is_some(self) -> typing.Literal[False]:
        """Check if the operation represented by this instance is Someful.
        .. code:: python
        >>> assert not Null(1).is_some()
        """
        return False

    def is_none(self) -> typing.Literal[True]:
        """Check if the operation represented by this instance is a Null.
        .. code:: python
        >>> assert Null(Exception()).is_none()
        """
        return True

    def ok_or_else(self, err: _E) -> Result[_T, _E]:
        """
        Transforms the Option<_T> into a Result<_T, _E>,
         mapping Some(v) to Success(v) and None to Failure(err()).
        .. code:: python
        >>> assert Some(1).ok_or_else(Exception()) == Success(1)
        >>> assert Null(1).ok_or_else(Exception()) == Failure(Exception())
        """
        return Result.from_failure(err)

    def bind(self, _: typing.Callable[[_T], Maybe[_T]]) -> Maybe[_T]:
        """
        Binds the current maybe to a function returning another maybe.
         Use this when the function intodruces side effects.
        .. code:: python
        >>> def factory(inner_value: int | None) -> Maybe[typing.Optional[int]]:
        ...     if inner_value > 0:
        ...         return Some(inner_value * 2)
        ...     return Null(inner_value)
        ...
        ... assert Some(10).bind(factory) == Some(20)
        ... assert Some(-10).bind(factory) == Null(None)
        """
        return self

    def map(self, _: typing.Callable[[_T], _T_new]) -> Maybe[_T]:
        """
        Binds the current maybe to a function returning another maybe.
         Use this when the function intodruces no side effects.
        .. code:: python
        >>> assert Some(10).map(bool) == Some(True)
        ... assert Null(10).bind(bool) == Null(None)
        """
        return self


Maybe = Some[_T] | Null[_T]

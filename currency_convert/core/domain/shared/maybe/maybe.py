import typing

_T_co = typing.TypeVar("_T_co", covariant=True, bound=typing.Any)
_N_co = typing.TypeVar("_N_co", covariant=True, bound=typing.Any)
_T_new = typing.TypeVar("_T_new")


@typing.runtime_checkable
class Maybe(typing.Protocol[_T_co, _N_co]):
    __slots__ = ("_inner_value",)

    _inner_value: _T_co | _N_co

    def __init__(self, inner_value: _T_co | _N_co) -> None:
        self._inner_value = inner_value

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, type(self))
            and self._inner_value == __value._inner_value
        )

    def __ne__(self, __value: object) -> bool:
        return not (self == __value)

    def value_or(
        self,
        default_value: _T_new,
    ) -> _T_co | _T_new:
        """Get value or default value.

        .. code:: python

        >>> assert Some(1).value_or(2) == 1
        >>> assert Null(1).value_or(2) == 2

        """

    def unwrap(self) -> _T_co:
        """Get value or None.

        .. code:: python

        >>> assert Some(1).unwrap() == 1

        >>> Null(1).unwrap() is None

        """

    @classmethod
    def from_value(
        cls,
        inner_value: _T_new,
    ) -> "Maybe[_T_new, typing.Any]":
        """One more value to create Some unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python

        >>> assert Maybe.from_value(1) == Some(1)

        You can use this method or :func:`~Some`,
        choose the most convenient for you.

        """
        return Some(inner_value)

    @classmethod
    def from_none(
        cls,
        inner_value: _N_co | _T_co,
    ) -> "Maybe[typing.Any, _N_co]":
        """One more value to create Null unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python

        >>> assert Maybe.from_none(1) == Null(1)

        You can use this method or :func:`Null`,
        choose the most convenient for you.

        """
        return Null(inner_value)

    def is_some(self) -> bool:
        """Check if the operation represented by this instance is Someful.

        .. code:: python

        >>> assert Maybe.from_value(1).is_some()
        """

    def is_none(self) -> bool:
        """Check if the operation represented by this instance is a Null.

        .. code:: python

        >>> assert Maybe.from_none(Exception()).is_none()
        """


@typing.final
class Some(Maybe[_T_co, typing.Any]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[_T_co]:
        yield self._inner_value

    def __repr__(self) -> str:
        return f"Some({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((True, self._inner_value))

    def __init__(self, inner_value: _T_co) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> _T_co:
        return self._inner_value  # type:ignore[no-any-return]

    def value_or(self, _: _T_new) -> _T_co:
        return self._inner_value  # type:ignore[no-any-return]

    def is_some(self) -> typing.Literal[True]:
        return True

    def is_none(self) -> typing.Literal[False]:
        return False


@typing.final
class Null(Maybe[None, _N_co]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[None]:
        yield None

    def __repr__(self) -> str:
        return f"Null({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((False, self._inner_value))

    def __init__(self, _: _N_co) -> None:
        super().__init__(None)

    def unwrap(self) -> None:
        return None

    def value_or(self, default_value: _T_new) -> _T_new:
        return default_value

    def is_some(self) -> typing.Literal[False]:
        return False

    def is_none(self) -> typing.Literal[True]:
        return True

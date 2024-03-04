import typing

from currency_convert.core.domain.shared.error import CurrencyConverterError

_T_co = typing.TypeVar("_T_co", covariant=True, bound=typing.Any)
_E_co = typing.TypeVar("_E_co", covariant=True, bound=Exception)
_T_new = typing.TypeVar("_T_new")


class UnwrapFailedError(CurrencyConverterError):
    """Unwrap failed error."""


@typing.runtime_checkable
class Result(typing.Protocol[_T_co, _E_co]):
    __slots__ = ("_inner_value",)

    _inner_value: _T_co | _E_co

    def __init__(self, inner_value: _T_co | _E_co) -> None:
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

        >>> from returns.result import Failure, Success
        >>> assert Success(1).value_or(2) == 1
        >>> assert Failure(1).value_or(2) == 2

        """

    def unwrap(self) -> _T_co:
        """Get value or raise exception.

        .. code:: python

        >>> from returns.result import Failure, Success
        >>> assert Success(1).unwrap() == 1

        >>> Failure(1).unwrap()
        Traceback (most recent call last):
        ...
        returns.primitives.exceptions.UnwrapFailedError

        """

    def failure(self) -> _E_co:
        """Get failed value or raise exception.

        .. code:: python

        >>> from returns.result import Failure, Success
        >>> assert Failure(1).failure() == 1

        >>> Success(1).failure()
            Traceback (most recent call last):
            ...
            returns.primitives.exceptions.UnwrapFailedError

        """

    @classmethod
    def from_value(
        cls,
        inner_value: _T_new,
    ) -> "Result[_T_new, typing.Any]":
        """One more value to create success unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python

        >>> from returns.result import Result, Success
        >>> assert Result.from_value(1) == Success(1)

        You can use this method or :func:`~Success`,
        choose the most convenient for you.

        """
        return Success(inner_value)

    @classmethod
    def from_failure(
        cls,
        inner_value: _E_co | _T_co,
    ) -> "Result[typing.Any, _E_co]":
        """One more value to create failure unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python

        >>> from returns.result import Result, Failure
        >>> assert Result.from_failure(1) == Failure(1)

        You can use this method or :func:`Failure`,
        choose the most convenient for you.

        """
        return Failure(inner_value)

    def is_success(self) -> bool:
        """Check if the operation represented by this instance is successful.

        .. code:: python

        >>> from returns.result import Result, Failure
        >>> assert Result.from_value(1).is_success()
        """

    def is_failure(self) -> bool:
        """Check if the operation represented by this instance is a failure.

        .. code:: python

        >>> from returns.result import Result, Failure
        >>> assert Result.from_failure(Exception()).is_failure()
        """


@typing.final
class Success(Result[_T_co, typing.Any]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __iter__(self) -> typing.Iterator[_T_co]:
        yield self._inner_value

    def __repr__(self) -> str:
        return f"Success({self._inner_value!r})"

    def __hash__(self) -> int:
        return hash((True, self._inner_value))

    def __init__(self, inner_value: _T_co) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> _T_co:
        return self._inner_value  # type:ignore[no-any-return]

    def value_or(self, _: _T_new) -> _T_co:
        return self._inner_value  # type:ignore[no-any-return]

    def failure(self) -> typing.NoReturn:
        raise UnwrapFailedError(self)

    def is_success(self) -> typing.Literal[True]:
        return True

    def is_failure(self) -> typing.Literal[False]:
        return False


@typing.final
class Failure(Result[typing.Any, _E_co]):
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

    def __init__(self, inner_value: _E_co) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> typing.NoReturn:
        match self._inner_value:
            case Exception():
                raise self._inner_value
            case _:
                raise UnwrapFailedError(self)

    def value_or(self, default_value: _T_new) -> _T_new:
        return default_value

    def failure(self) -> _E_co:
        return self._inner_value

    def is_success(self) -> typing.Literal[False]:
        return False

    def is_failure(self) -> typing.Literal[True]:
        return True

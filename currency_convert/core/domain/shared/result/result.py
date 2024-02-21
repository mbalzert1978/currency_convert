import typing

from currency_convert.core.domain.shared.error import CurrencyConverterError

_T_co = typing.TypeVar("_T_co", covariant=True, bound=typing.Any)
_E_co = typing.TypeVar("_E_co", covariant=True, bound=Exception)
_T_new = typing.TypeVar("_T_new")


class UnwrapFailedError(CurrencyConverterError):
    """Unwrap failed error."""

    @classmethod
    def from_exception(cls, exc: Exception) -> typing.NoReturn:
        raise cls from exc


class Result(typing.Protocol[_T_co, _E_co]):
    __slots__ = ("_inner_value",)

    _inner_value: _T_co | _E_co

    def __init__(self, inner_value: _T_co | _E_co) -> None:
        self._inner_value = inner_value

    def value_or(
        self,
        default_value: _T_new,
    ) -> _T_co | _T_new:
        """
        Get value or default value.

        .. code:: python

        >>> from returns.result import Failure, Success
        >>> assert Success(1).value_or(2) == 1
        >>> assert Failure(1).value_or(2) == 2

        """

    def unwrap(self) -> _T_co:
        """
        Get value or raise exception.

        .. code:: python

        >>> from returns.result import Failure, Success
        >>> assert Success(1).unwrap() == 1

        >>> Failure(1).unwrap()
        Traceback (most recent call last):
        ...
        returns.primitives.exceptions.UnwrapFailedError

        """

    def failure(self) -> _E_co:
        """
        Get failed value or raise exception.

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
        """
        One more value to create success unit values.

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
    ) -> "Result[typing.Any, Exception]":
        """
        One more value to create failure unit values.

        It is useful as a united way to create a new value from any container.

        .. code:: python

        >>> from returns.result import Result, Failure
        >>> assert Result.from_failure(1) == Failure(1)

        You can use this method or :func:`Failure`,
        choose the most convenient for you.

        """
        return Failure(inner_value)

    def is_success(self) -> bool:
        """
        Check if the operation represented by this instance is successful.

        .. code:: python

        >>> from returns.result import Result, Failure
        >>> assert Result.from_value(1).is_success()
        """

    def is_failure(self) -> bool:
        """
        Check if the operation represented by this instance is a failure.

        .. code:: python

        >>> from returns.result import Result, Failure
        >>> assert Result.from_failure(Exception()).is_failure()
        """


@typing.final
class Success(Result[_T_co, typing.Any]):
    __slots__ = ("_inner_value",)
    __match_args__ = ("_inner_value",)

    def __init__(self, inner_value: _T_co) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> _T_co:
        return self._inner_value

    def value_or(self, _: _T_new) -> _T_co:
        return self._inner_value

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

    def __init__(self, inner_value: _E_co) -> None:
        super().__init__(inner_value)

    def unwrap(self) -> _E_co:
        match self._inner_value:
            case Exception():
                UnwrapFailedError.from_exception(self._inner_value)
            case _:
                UnwrapFailedError.from_exception(Exception(self))

    def value_or(self, default_value: _T_new) -> _T_new:
        return default_value

    def failure(self) -> _E_co:
        return self._inner_value

    def is_success(self) -> typing.Literal[False]:
        return False

    def is_failure(self) -> typing.Literal[True]:
        return True

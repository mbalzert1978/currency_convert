import typing

T = typing.TypeVar("T")


class CurrencyConverterError(Exception):
    """Base class for exceptions raised by the CurrencyConverter class."""


class Error(CurrencyConverterError):
    def __init__(self, code: int, detail: str, *args: object) -> None:
        self._code = code
        self._detail = detail
        super().__init__(*args)

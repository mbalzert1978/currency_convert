import typing

T = typing.TypeVar("T")


class Error(Exception):
    def __init__(self, code: int, detail: str, *args: object) -> None:
        self._code = code
        self._detail = detail
        super().__init__(*args)

    @classmethod
    def none(cls) -> typing.Self:
        return cls(code=500, detail="Internal Server Error")

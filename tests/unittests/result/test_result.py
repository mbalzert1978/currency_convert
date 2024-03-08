import pytest

from currency_convert.core.domain.shared.returns.returns import (
    Failure,
    Option,
    Result,
    Success,
    UnwrapFailedError,
)


def test_init() -> None:
    r = Result.from_value("yay")
    e = Result.from_failure("oh no")

    assert r.unwrap() == "yay"
    with pytest.raises(UnwrapFailedError):
        e.unwrap() == "oh no"


def test_equality() -> None:
    assert Success(1) == Success(1)
    assert Failure(1) == Failure(1)
    assert Success(1) != Failure(1)
    assert Success(1) != Success(2)
    assert Failure(1) != Failure(2)
    assert Success(1) == Success(1)
    assert Success(1) != "abc"
    assert Success("0") != Success(0)


def test_hash() -> None:
    assert len({Success(1), Failure("2"), Success(1), Failure("2")}) == 2
    assert len({Success(1), Success(2)}) == 2
    assert len({Success("a"), Failure("a")}) == 2


def test_repr() -> None:
    o = Success(123)
    n = Failure(-1)

    assert repr(o) == "Success(123)"
    assert o == eval(repr(o))

    assert repr(n) == "Failure(-1)"
    assert n == eval(repr(n))


def test_unwrap() -> None:
    assert Result.from_value(1).unwrap() == 1

    with pytest.raises(UnwrapFailedError):
        Result.from_failure(1).unwrap()


def test_value_or() -> None:
    assert Result.from_value(1).value_or(2) == 1
    assert Result.from_failure(1).value_or(2) == 2


def test_failure() -> None:
    assert Result.from_failure(1).failure() == 1

    with pytest.raises(UnwrapFailedError):
        Result.from_value(1).failure()


def test_is_success() -> None:
    assert Result.from_value(1).is_success()
    assert not Result.from_failure(1).is_success()


def test_is_failure() -> None:
    assert Result.from_failure(1).is_failure()
    assert not Result.from_value(1).is_failure()


def test_ok() -> None:
    assert Result.from_value(1).ok() == Option.from_value(1)
    assert Result.from_failure(1).ok() == Option.from_none(1)


def test_bind() -> None:
    class Parser:
        def __init__(self) -> None:
            self._exc = None

        def __call__(self, f):
            try:
                return Result.from_value(int(f))
            except ValueError as exc:
                self._exc = exc
                return Result.from_failure(exc)

    parse = Parser()
    assert Result.from_value("10").bind(parse) == Result.from_value(10)
    assert Result.from_value("foo").bind(parse) == Result.from_failure(parse._exc)


def test_map() -> None:
    assert Result.from_value(10).map(bool) == Result.from_value(True)
    assert Result.from_failure(10).map(bool) == Result.from_failure(10)


def test_map_or() -> None:
    assert Result.from_value("foo").map_or(42, len) == 3
    assert Result.from_failure("bar").map_or(42, len) == 42


def test_pattern_matching_success_type() -> None:
    o = Result.from_value("yay")
    match o:
        case Success(value):
            reached = True

    assert value == "yay"
    assert reached


def test_pattern_matching_failure_type() -> None:
    n = Result.from_failure("nay")
    match n:
        case Failure(value):
            reached = True

    assert value == "nay"
    assert reached


def test_slots() -> None:
    o = Success("yay")
    n = Failure("nay")
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]

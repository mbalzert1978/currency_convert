import typing

import pytest

from currency_convert.core.domain.shared.returns import Null, Option, Result, Some


def test_init() -> None:
    o = Option.from_value(1)
    n = Option.from_none(1)

    assert o == Some(1)
    assert n == Null(1)


def test_pattern_matching_Some_type() -> None:
    o = Option.from_value("yay")
    match o:
        case Some(value):
            reached = True

    assert value == "yay"
    assert reached


def test_pattern_matching_Null_type() -> None:
    n = Option.from_none("nay")
    match n:
        case Null(value):
            reached = True

    assert value is None
    assert reached


def test_slots() -> None:
    o = Option.from_value("yay")
    n = Option.from_none("nay")
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]


def test_equality() -> None:
    assert Option.from_value(1) == Option.from_value(1)
    assert Option.from_none(1) == Option.from_none(1)
    assert Option.from_value(1) != Option.from_none(1)
    assert Option.from_value(1) != Option.from_value(2)
    assert Option.from_none(1) == Option.from_none(2)
    assert Option.from_value(1) == Option.from_value(1)
    assert Option.from_value(1) != "abc"
    assert Option.from_value("0") != Option.from_value(0)


def test_hash() -> None:
    assert (
        len(
            {
                Option.from_value(1),
                Option.from_none("2"),
                Option.from_value(1),
                Option.from_none("2"),
            }
        )
        == 2
    )
    assert len({Option.from_value(1), Option.from_value(2)}) == 2
    assert len({Option.from_value("a"), Option.from_none("a")}) == 2


def test_repr() -> None:
    o = Some(123)
    n = Null(-1)

    assert repr(o) == "Some(123)"
    assert o == eval(repr(o))

    assert repr(n) == "Null(None)"
    assert n == eval(repr(n))


def test_unwrap() -> None:
    assert Option.from_value(1).unwrap() == 1
    assert Option.from_none(1).unwrap() is None


def test_value_or() -> None:
    assert Option.from_value(1).value_or(2) == 1
    assert Option.from_none(1).value_or(2) == 2


def test_is_some() -> None:
    assert Option.from_value(1).is_some()
    assert not Option.from_none(1).is_some()


def test_is_none() -> None:
    assert not Option.from_value(1).is_none()
    assert Option.from_none(1).is_none()


def test_ok_or_else() -> None:
    assert Option.from_value(1).ok_or_else("Foo") == Result.from_value(1)
    assert Option.from_none(1).ok_or_else("Foo") == Result.from_failure("Foo")


def test_bind() -> None:
    def mul_two(f: typing.Optional[int]) -> Option[int]:
        return Null(f) if f is None else Some(f * 2)  # type: ignore[arg-type]

    assert Option.from_value(10).bind(mul_two) == Option.from_value(20)
    assert Option.from_none(-10).bind(mul_two) == Option.from_none(None)


def test_map() -> None:
    assert Option.from_value(10).map(bool) == Option.from_value(True)
    assert Option.from_none(10).map(bool) == Option.from_none(None)


def test_map_or() -> None:
    assert Option.from_value("foo").map_or(42, len) == 3
    assert Option.from_none("bar").map_or(42, len) == 42

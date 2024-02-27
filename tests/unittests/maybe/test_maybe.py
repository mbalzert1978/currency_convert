import pytest

from currency_convert.core.domain.shared.maybe import Maybe, Some, Null


def test_unwrap() -> None:
    assert Some(1).unwrap() == 1

    assert Null(1).unwrap() is None


def test_value_or() -> None:
    assert Some(1).value_or(2) == 1
    assert Null(1).value_or(2) == 2


def test_is_Some() -> None:
    assert Some(1).is_some()
    assert not Null(1).is_some()


def test_is_Null() -> None:
    assert not Some(1).is_none()
    assert Null(1).is_none()


def test_pattern_matching_Some_type() -> None:
    o = Maybe.from_value("yay")
    match o:
        case Some(value):
            reached = True

    assert value == "yay"
    assert reached


def test_pattern_matching_Null_type() -> None:
    n = Maybe.from_none("nay")
    match n:
        case Null(value):
            reached = True

    assert value is None
    assert reached


def test_slots() -> None:
    o = Some("yay")
    n = Null("nay")
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]


def test_equality() -> None:
    assert Some(1) == Some(1)
    assert Null(1) == Null(1)
    assert Some(1) != Null(1)
    assert Some(1) != Some(2)
    assert Null(1) == Null(2)
    assert Some(1) == Some(1)
    assert Some(1) != "abc"
    assert Some("0") != Some(0)


def test_hash() -> None:
    assert len({Some(1), Null("2"), Some(1), Null("2")}) == 2
    assert len({Some(1), Some(2)}) == 2
    assert len({Some("a"), Null("a")}) == 2


def test_repr() -> None:
    o = Some(123)
    n = Null(-1)

    assert repr(o) == "Some(123)"
    assert o == eval(repr(o))

    assert repr(n) == "Null(None)"
    assert n == eval(repr(n))

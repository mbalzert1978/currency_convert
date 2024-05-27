import decimal

from currency_convert.domain.agency.valueobjects.money import Money


def test_create_ok() -> None:
    result = Money.create(100)

    assert result.is_ok()
    assert result.unwrap() == Money(decimal.Decimal("100.00000000"))

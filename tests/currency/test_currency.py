import datetime
import uuid

import pydantic
import pytest

from currency_convert.core.domain.currency.code import CurrencyCode
from currency_convert.core.domain.currency.entity import Currency
from currency_convert.core.domain.shared.uuid_valueobject import UUIDID


def test_create() -> None:
    c = Currency.create("USD", "US Dollar")

    assert isinstance(c.code, CurrencyCode)
    assert isinstance(c.id_, UUIDID)
    assert isinstance(c.id_.value, uuid.UUID)
    assert isinstance(c.created_at, datetime.datetime)
    assert isinstance(c.updated_at, datetime.datetime)

    assert c.code.value == "USD"
    assert c.created_at.tzinfo == datetime.timezone.utc
    assert c.updated_at.tzinfo == datetime.timezone.utc


def test_create_invalid_code() -> None:
    with pytest.raises(pydantic.ValidationError, match="Invalid value:"):
        _ = Currency.create("To_long", "US Dollar")

    with pytest.raises(pydantic.ValidationError):
        _ = Currency.create(None, "US Dollar")

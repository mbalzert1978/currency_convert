import decimal
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Currency(BaseModel):
    code: str = Field(max_length=3, min_length=3)


class Money(BaseModel):
    amount: decimal.Decimal = Field(gt=0)


class Rate(BaseModel):
    currency_from: Currency
    currency_to: Currency
    rate: Money
    iso_8601: str


class Product(Generic[T], BaseModel):
    data: T


class Products(Generic[T], BaseModel):
    data: list[T]

import decimal
from typing import Generic, TypeVar
import uuid

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


class Agency(BaseModel):
    id: uuid.UUID
    name: str
    base: Currency
    address: str
    country: str
    rates: list[Rate]


class Product(BaseModel, Generic[T]):
    data: T


class Products(BaseModel, Generic[T]):
    data: list[T]

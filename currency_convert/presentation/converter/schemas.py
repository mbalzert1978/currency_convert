import decimal
import uuid
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, model_validator

T = TypeVar("T")


class Currency(BaseModel):
    code: str = Field(max_length=3, min_length=3)


class Money(BaseModel):
    amount: decimal.Decimal = Field(gt=0)


class Rate(BaseModel):
    currency_from: Currency
    currency_to: Currency
    rate: Money
    dt: str | None = None


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
    count: int = Field(default=0, init=False)

    @model_validator(mode="before")
    @classmethod
    def set_count(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["count"] = len(data.get("data", 0))
        return data

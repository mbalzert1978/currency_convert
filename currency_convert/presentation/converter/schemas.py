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
    iso_8601: str | None = None

    @model_validator(mode="before")
    @classmethod
    def extract_iso(cls, data: dict[str, Any]) -> Any:
        try:
            data["iso_8601"] = data.pop("date").isoformat()
        except AttributeError as exc:
            raise ValueError(f"Expected datetime, got {data}") from exc
        else:
            return data


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

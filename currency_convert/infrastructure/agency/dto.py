from __future__ import annotations

import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata = MetaData(
    naming_convention={
        "ix": "%(column_0_label)s_idx",
        "uq": "%(table_name)s_%(column_0_name)s_key",
        "ck": "%(table_name)s_%(constraint_name)s_check",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    }
)


class Base(DeclarativeBase):
    metadata = metadata


class Rate(Base):
    __tablename__ = "rates"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    currency_from: Mapped[str] = mapped_column()
    currency_to: Mapped[str] = mapped_column()
    rate: Mapped[Decimal] = mapped_column()
    date: Mapped[datetime.datetime] = mapped_column()
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"))
    agency: Mapped[Agency] = relationship(back_populates="rates")


class Agency(Base):
    __tablename__ = "agencies"
    id: Mapped[str] = mapped_column(primary_key=True)
    base: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    rates: Mapped[set[Rate]] = relationship(
        back_populates="agency",
        cascade="all, delete-orphan",
    )

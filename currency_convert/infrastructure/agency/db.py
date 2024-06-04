from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class MappedRate(Base):
    __tablename__ = "rates"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    currency_from: Mapped[str] = mapped_column()
    currency_to: Mapped[str] = mapped_column()
    rate: Mapped[Decimal] = mapped_column()
    date: Mapped[str] = mapped_column()
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"))
    agency: Mapped[MappedAgency] = relationship(back_populates="rates")


class MappedAgency(Base):
    __tablename__ = "agencies"
    id: Mapped[str] = mapped_column(primary_key=True)
    base: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    rates: Mapped[list[MappedRate]] = relationship(
        back_populates="agency",
        cascade="all, delete-orphan",
    )

from __future__ import annotations

from decimal import Decimal

from results import Result
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm.session import Session

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
)
from currency_convert.domain.agency.valueobjects.rate import Rate


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
        back_populates="agency", cascade="all, delete-orphan"
    )


class MemoryAgency:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, agency_id: str) -> Result[Agency, AgencyNotFoundError]:
        result = self.session.get(MappedAgency, agency_id)
        if result is None:
            return Result.Err(AgencyNotFoundError("Agency not found"))
        return Result.Ok(map_mapped_agency(result))

    def find_by_name(self, name: str) -> Result[Agency, AgencyNotFoundError]:
        result = self.session.query(MappedAgency).filter_by(name=name).first()
        if result is None:
            return Result.Err(AgencyNotFoundError("Agency not found"))
        return Result.Ok(map_mapped_agency(result))

    def find_all(self) -> Result[list[Agency], AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(MappedAgency).all)
            .map(lambda agencies: list(map_mapped_agency(a) for a in agencies))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def save(self, agency: Agency) -> Result[Agency, Exception]:
        self.session.merge(map_agency(agency))
        try:
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            return Result.Err(exc)
        else:
            return Result.Ok(agency)


def map_agency(agency: Agency) -> MappedAgency:
    return MappedAgency(
        id=agency.id.hex,
        base=next(agency.base.get_values()),
        name=agency.name,
        address=agency.address,
        country=agency.country,
        rates=[map_rate(rate) for rate in agency.rates],
    )


def map_rate(rate: Rate) -> MappedRate:
    return MappedRate(
        currency_from=next(rate.currency_from.get_values()),
        currency_to=next(rate.currency_to.get_values()),
        rate=next(rate.rate.get_values()),
        date=rate.date.isoformat(),
    )


def map_mapped_agency(mapped: MappedAgency) -> Agency:
    return Agency.from_attributes(
        mapped.id,
        mapped.base,
        mapped.name,
        mapped.address,
        mapped.country,
        [map_mapped_rate(rate) for rate in mapped.rates],
    )


def map_mapped_rate(mapped: MappedRate) -> Rate:
    return Rate.from_attributes(
        mapped.id,
        mapped.currency_from,
        mapped.currency_to,
        mapped.rate,
        mapped.date,
    )

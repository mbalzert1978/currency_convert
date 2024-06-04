from __future__ import annotations

from results import Result
from sqlalchemy.orm.session import Session

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
)
from currency_convert.infrastructure.db import MappedAgency
from currency_convert.infrastructure.mapper import map_agency, map_mapped_agency


class AgencyRepo:
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

from __future__ import annotations

from results import Result
from sqlalchemy.orm.session import Session

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
)
from currency_convert.infrastructure.agency.db import MappedAgency
from currency_convert.infrastructure.agency.mapper import AgencyMapper


class AgencyRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, id: str) -> Result[Agency, AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(MappedAgency).filter_by(id=id).one)
            .and_then(lambda agency: Result.from_fn(AgencyMapper.from_db, agency))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def find_by_name(self, name: str) -> Result[Agency, AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(MappedAgency).filter_by(name=name).one)
            .and_then(lambda agency: Result.from_fn(AgencyMapper.from_db, agency))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def find_all(self) -> Result[list[Agency], AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(MappedAgency).all)
            .map(lambda rows: list(AgencyMapper.from_db(agency) for agency in rows))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def save(self, agency: Agency) -> Result[Agency, Exception]:
        try:
            self.session.merge(AgencyMapper.into_db(agency))
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            return Result.Err(exc)
        else:
            return Result.Ok(agency)

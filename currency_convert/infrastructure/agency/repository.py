from __future__ import annotations

from results import Result
from sqlalchemy.orm.session import Session

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
)
from currency_convert.infrastructure.agency import dto
from currency_convert.infrastructure.agency.mapper import AgencyMapper


class AgencyRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, id: str) -> Result[Agency, AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(dto.Agency).filter_by(id=id).one)
            .and_then(lambda agency: Result.from_fn(AgencyMapper.from_db, agency))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def find_by_name(self, name: str) -> Result[Agency, AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(dto.Agency).filter_by(name=name).one)
            .and_then(lambda agency: Result.from_fn(AgencyMapper.from_db, agency))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def find_all(self) -> Result[list[Agency], AgencyNotFoundError]:
        return (
            Result.from_fn(self.session.query(dto.Agency).all)
            .map(lambda rows: list(AgencyMapper.from_db(agency) for agency in rows))
            .map_err(AgencyNotFoundError.from_exc)
        )

    def save(self, agency: Agency) -> Result[Agency, Exception]:
        def _rollback(exc: Exception) -> Exception:
            if (err := Result.from_fn(self.session.rollback)).is_err():
                return err.unwrap_err()
            return exc

        return (
            Result.from_fn(AgencyMapper.into_db, agency)
            .and_then(lambda mapped: Result.from_fn(self.session.merge, mapped))
            .and_then(lambda _: Result.from_fn(self.session.commit))
            .map(lambda _: agency)
            .map_err(_rollback)
        )

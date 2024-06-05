from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
    AgencySaveError,
)
from currency_convert.infrastructure.agency import dto
from currency_convert.infrastructure.agency.mapper import AgencyMapper


class AgencyRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, id: str) -> Agency:
        if (a := self.session.query(dto.Agency).filter_by(id=id).first()) is None:
            raise AgencyNotFoundError()
        return AgencyMapper.from_db(a)

    def find_by_name(self, name: str) -> Agency:
        if (a := self.session.query(dto.Agency).filter_by(name=name).first()) is None:
            raise AgencyNotFoundError()
        return AgencyMapper.from_db(a)

    def find_all(self) -> list[Agency]:
        return list(
            AgencyMapper.from_db(agency)
            for agency in self.session.query(dto.Agency).all()
        )

    def save(self, agency: Agency) -> None:
        try:
            self.session.merge(AgencyMapper.into_db(agency))
            self.session.commit()
        except SQLAlchemyError as exc:
            self.session.rollback()
            raise AgencySaveError.from_exc(exc)

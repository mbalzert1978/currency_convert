from __future__ import annotations

from currency_convert.domain.agency.entities.agency import (
    Agency,
    AgencyNotFoundError,
    AgencySaveError,
)


class AgencyRepo:
    def __init__(self, agencies: set[Agency] | None = None) -> None:
        self.agencies = agencies or set()

    def find_by_id(self, id: str) -> Agency:
        if (agency := next((a for a in self.agencies if a.id == id), None)) is None:
            raise AgencyNotFoundError()
        return agency

    def find_by_name(self, name: str) -> Agency:
        if (agency := next((a for a in self.agencies if a.name == name), None)) is None:
            raise AgencyNotFoundError()
        return agency

    def find_all(self) -> list[Agency]:
        return list(self.agencies)

    def save(self, agency: Agency) -> None:
        try:
            self.agencies.discard(next(a for a in self.agencies if a.id == agency.id))
            self.agencies.add(agency)
        except StopIteration as exc:
            raise AgencySaveError from exc

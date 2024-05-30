import typing
import uuid

from results import Result

from currency_convert.domain.agency.entities.agency import Agency
from currency_convert.domain.primitives.error import GenericError


class AgencyRepository(typing.Protocol):
    def create(
        self,
        base: str,
        name: str,
        address: str,
        country: str,
    ) -> Result[uuid.UUID, GenericError]:
        pass

    def find_by_id(self, agency_id: str) -> Result[Agency, GenericError]:
        pass

    def find_by_name(self, name: str) -> Result[Agency, GenericError]:
        pass

    def find_all(self) -> Result[list[Agency], GenericError]:
        pass

from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.agency.update.command import UpdateAgency
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Failure, Result, Success
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID


class UpdateAgencyHandler(CommandHandler[UpdateAgency, Result[UUIDID, Error]]):
    def __init__(self, agency_repository: IAgencyRepository) -> None:
        self._agency_repository = agency_repository

    def handle(self, cmd: UpdateAgency) -> Result[UUIDID, Error]:
        match self._agency_repository.find_by_name(cmd.name):
            case Success(in_db):
                into_db = Agency.update(**in_db.model_dump())
            case Failure(exc):
                return Result.from_failure(exc)

        with self._agency_repository as repo:
            db_result = repo.update(into_db)

        if db_result.is_failure():
            return Result.from_failure(db_result)
        return Result.from_value(into_db.id_)

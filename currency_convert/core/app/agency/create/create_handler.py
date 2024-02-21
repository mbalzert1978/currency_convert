from currency_convert.core.app.abstractions.command_handler import CommandHandler
from currency_convert.core.app.agency.create.create_command import CreateAgencyCommand
from currency_convert.core.domain.agency.agency_repository import IAgencyRepository
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.agency.errors import AgencyAllreadExistsError
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result
from currency_convert.core.domain.shared.value_objects.uuidid import UUIDID

EXIST_MSG = "Agency with name %s already exists."


class CreateAgencyCommandHandler(CommandHandler[CreateAgencyCommand, Result[UUIDID, Error]]):
    def __init__(self, agency_repository: IAgencyRepository) -> None:
        self._agency_repository = agency_repository

    def handle(self, cmd: CreateAgencyCommand) -> Result[UUIDID, Error]:
        if self._agency_repository.find_by_name(cmd.name).is_success():
            return Result.from_failure(AgencyAllreadExistsError(409, detail=EXIST_MSG % cmd.name))

        into_db = Agency.create(
            name=cmd.name,
            base_currency=cmd.base_currency,
            residing_country=cmd.residing_country,
        )

        with self._agency_repository as repo:
            db_result = repo.add(into_db)

        if db_result.is_failure():
            return Result.from_failure(db_result)
        return Result.from_value(into_db.id_)

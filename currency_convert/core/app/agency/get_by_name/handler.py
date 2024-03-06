from http import HTTPStatus

from currency_convert.core.app.abstractions.query_handler import QueryHandler
from currency_convert.core.app.agency.get_by_name.query import GetAgencyByName
from currency_convert.core.domain.agency.entity import Agency
from currency_convert.core.domain.agency.errors import AgencyNotFoundError
from currency_convert.core.domain.resources import strings_error
from currency_convert.core.domain.shared.adapter.sql_alchemy_adapter import QueryAdapter
from currency_convert.core.domain.shared.error import Error
from currency_convert.core.domain.shared.result.result import Result


class GetAgencyByNameHandler(QueryHandler[GetAgencyByName, Result[Agency, Error]]):
    QUERY = """
    SELECT
        a.id,
        a.name,
        a.base_currency,
        a.created_at,
        a.updated_at
    FROM
        agency AS a
    WHERE
        name = %(name)s;
    """

    def __init__(self, query_adapter: QueryAdapter) -> None:
        self._query_adapter = query_adapter

    def handle(self, cmd: GetAgencyByName) -> Result[Agency, Error]:
        with self._query_adapter as adapter:
            query_result = adapter.execute(self.QUERY, dict(name=cmd.name))
        if query_result.is_failure():
            return Result.from_failure(query_result.failure())
        if not query_result.unwrap():
            return Result.from_failure(
                AgencyNotFoundError(
                    HTTPStatus.NOT_FOUND,
                    strings_error.NOT_FOUND % ("Name", cmd.name),
                )
            )
        return Result.from_value(Agency.model_validate(query_result.unwrap()))

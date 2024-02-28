from currency_convert.core.domain.shared.query import Query


class GetAgencyByName(Query):
    name: str

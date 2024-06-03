from currency_convert.domain.agency.entities.interface import UnprocessedRate


INSERTS = [
    UnprocessedRate(
        currency_from="EUR",
        currency_to="USD",
        rate=1.1,
        date="2021-01-01",
    ),
    UnprocessedRate(
        currency_from="EUR",
        currency_to="GBP",
        rate=0.8,
        date="2021-01-01",
    ),
    UnprocessedRate(
        currency_from="EUR",
        currency_to="RUB",
        rate=0.9,
        date="2021-01-01",
    ),
]

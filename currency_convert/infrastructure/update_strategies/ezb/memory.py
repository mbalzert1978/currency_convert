from currency_convert.domain.agency.entities.interface import UnprocessedRate


class EzbMemoryUpdateStrategy:
    def __init__(self, rates: list[UnprocessedRate]) -> None:
        self.rates: list[UnprocessedRate] = rates or []

    def __call__(self) -> list[UnprocessedRate]:
        return self.rates

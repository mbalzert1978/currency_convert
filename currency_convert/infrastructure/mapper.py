from currency_convert.domain.agency.entities.agency import Agency
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.infrastructure.db import MappedAgency, MappedRate


def map_agency(agency: Agency) -> MappedAgency:
    return MappedAgency(
        id=agency.id.hex,
        base=next(agency.base.get_values()),
        name=agency.name,
        address=agency.address,
        country=agency.country,
        rates=[map_rate(rate) for rate in agency.rates],
    )


def map_rate(rate: Rate) -> MappedRate:
    return MappedRate(
        currency_from=next(rate.currency_from.get_values()),
        currency_to=next(rate.currency_to.get_values()),
        rate=next(rate.rate.get_values()),
        date=rate.date.isoformat(),
    )


def map_mapped_agency(mapped: MappedAgency) -> Agency:
    return Agency.from_attributes(
        mapped.id,
        mapped.base,
        mapped.name,
        mapped.address,
        mapped.country,
        [map_mapped_rate(rate) for rate in mapped.rates],
    )


def map_mapped_rate(mapped: MappedRate) -> Rate:
    return Rate.from_attributes(
        mapped.id,
        mapped.currency_from,
        mapped.currency_to,
        mapped.rate,
        mapped.date,
    )

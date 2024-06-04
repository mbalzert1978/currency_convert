from currency_convert.domain.agency.entities.agency import Agency
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.infrastructure.agency.db import DTOAgency, DTORate


class AgencyMapper:
    @staticmethod
    def into_db(agency: Agency) -> DTOAgency:
        return DTOAgency(
            id=agency.id.hex,
            base=next(agency.base.get_values()),
            name=agency.name,
            address=agency.address,
            country=agency.country,
            rates=[AgencyMapper._into_db_rate(rate) for rate in agency.rates],
        )

    @staticmethod
    def from_db(mapped: DTOAgency) -> Agency:
        return Agency.from_attributes(
            mapped.id,
            mapped.base,
            mapped.name,
            mapped.address,
            mapped.country,
            [AgencyMapper._from_db_rate(rate) for rate in mapped.rates],
        )

    @staticmethod
    def _into_db_rate(rate: Rate) -> DTORate:
        return DTORate(
            currency_from=next(rate.currency_from.get_values()),
            currency_to=next(rate.currency_to.get_values()),
            rate=next(rate.rate.get_values()),
            date=rate.date.isoformat(),
        )

    @staticmethod
    def _from_db_rate(mapped: DTORate) -> Rate:
        return Rate.from_attributes(
            mapped.id,
            mapped.currency_from,
            mapped.currency_to,
            mapped.rate,
            mapped.date,
        )

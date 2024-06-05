from currency_convert.domain.agency.entities.agency import Agency
from currency_convert.domain.agency.valueobjects.rate import Rate
from currency_convert.infrastructure.agency import dto


class AgencyMapper:
    @staticmethod
    def into_db(agency: Agency) -> dto.Agency:
        return dto.Agency(
            id=agency.id.hex,
            base=next(agency.base.get_values()),
            name=agency.name,
            address=agency.address,
            country=agency.country,
            rates={AgencyMapper._into_db_rate(rate) for rate in agency.rates},
        )

    @staticmethod
    def from_db(mapped: dto.Agency) -> Agency:
        return Agency.from_attributes(
            mapped.id,
            mapped.base,
            mapped.name,
            mapped.address,
            mapped.country,
            {AgencyMapper._from_db_rate(rate) for rate in mapped.rates},
        )

    @staticmethod
    def _into_db_rate(rate: Rate) -> dto.Rate:
        return dto.Rate(
            currency_from=next(rate.currency_from.get_values()),
            currency_to=next(rate.currency_to.get_values()),
            rate=next(rate.rate.get_values()),
            date=rate.dt,
        )

    @staticmethod
    def _from_db_rate(mapped: dto.Rate) -> Rate:
        return Rate.from_attributes(
            mapped.id,
            mapped.currency_from,
            mapped.currency_to,
            str(mapped.rate),
            mapped.date,
        )

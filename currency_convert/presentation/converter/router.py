import logging

from fastapi import APIRouter, HTTPException
from results import Err, Ok

from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.domain.agency.entities.agency import (
    AgencyNotFoundError,
    RateNotFoundError,
)
from currency_convert.presentation.converter.dependencies import FetchAllDep
from currency_convert.presentation.converter.schemas import Products, Rate

_logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{agency_name}/rates", response_model=Products[Rate])
def api_get_rates(
    agency_name: str,
    handler: FetchAllDep[FetchAll, tuple[Rate, ...], AgencyNotFoundError],
) -> Products[Rate]:
    cmd = FetchAll(agency_name=agency_name)
    match handler.execute(cmd):
        case Ok(rates):
            return Products(data=rates)
        case Err(err):
            match err:
                case AgencyNotFoundError():
                    raise HTTPException(status_code=404, detail="Agency not found")
                case RateNotFoundError():
                    raise HTTPException(status_code=404, detail="Rate not found")
                case _:
                    _logger.error(err)
                    raise HTTPException(
                        status_code=500, detail="Internal server error."
                    )
        case _:
            _logger.critical("Unreachable code path.")
            raise HTTPException(status_code=500, detail="Internal server error.")

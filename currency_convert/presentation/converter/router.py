import logging

from fastapi import APIRouter, HTTPException
from results import Err, Ok

from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.domain.agency.entities.agency import (
    AgencyCreationError,
    AgencyNotFoundError,
    RateNotFoundError,
)
from currency_convert.presentation.converter.dependencies import (
    FetchAllDep,
    CreationHandlerDep,
)
from currency_convert.presentation.converter.schemas import (
    Products,
    Rate,
    Product,
    Agency,
)

_logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{agency_name}/create", status_code=201)
def api_update(
    agency_name: str, base: str, url: str, country: str, handler: CreationHandlerDep
) -> Product[Agency]:
    cmd = CreateAgency(agency_name, base, url, country)
    match handler.execute(cmd):
        case Ok(agency):
            return Product(data=agency)
        case Err(err):
            match err:
                case AgencyCreationError():
                    raise HTTPException(status_code=409, detail=str(err))
                case _:
                    _logger.error(err)
                    raise HTTPException(
                        status_code=500, detail="Internal server error."
                    )
        case _:
            _logger.critical("Unreachable code path.")
            raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/{agency_name}/rates", response_model=Products[Rate])
def api_get_rates(agency_name: str, handler: FetchAllDep) -> Products[Rate]:
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

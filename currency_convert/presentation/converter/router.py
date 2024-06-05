import logging
from dataclasses import asdict
from typing import Literal

from fastapi import APIRouter, HTTPException

from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.application.agency.commands.update.command import UpdateByName
from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.domain.agency.entities.agency import (
    AgencyCreationError,
    AgencyNotFoundError,
    RateNotFoundError,
)
from currency_convert.presentation.converter.dependencies import (
    CreationHandlerDep,
    FetchAllDep,
    UpdateHandlerByNameDep,
    UpdateStrategyDep,
)
from currency_convert.presentation.converter.schemas import (
    Agency,
    Product,
    Products,
    Rate,
)

_logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{agency_name}/create", status_code=201)
def api_create_agency(
    agency_name: str, base: str, url: str, country: str, handler: CreationHandlerDep
) -> Product[Agency]:
    cmd = CreateAgency(agency_name, base, url, country)
    try:
        result = handler.execute(cmd)
    except Exception as e:
        _logger.critical("Unreachable code path.")
        raise HTTPException(status_code=500, detail="Internal server error.") from e
    else:
        return Product(data=result)


@router.put("/{agency_name}/update", status_code=200)
def api_update(
    agency_name: str, strategy: UpdateStrategyDep, handler: UpdateHandlerByNameDep
) -> Literal[200]:
    cmd = UpdateByName(strategy, agency_name)
    try:
        handler.execute(cmd)
    except Exception as e:
        _logger.critical("Unreachable code path.")
        raise HTTPException(status_code=500, detail="Internal server error.") from e
    else:
        return 200


@router.get("/{agency_name}/rates", response_model=Products[Rate])
def api_get_rates(agency_name: str, handler: FetchAllDep) -> Products[Rate]:
    cmd = FetchAll(agency_name=agency_name)
    try:
        rates = handler.execute(cmd)
    except Exception as e:
        _logger.critical("Unreachable code path.")
        raise HTTPException(status_code=500, detail="Internal server error.") from e
    else:
        return Products(data=[Rate(**asdict(rate)) for rate in rates])

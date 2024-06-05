import logging
from dataclasses import asdict
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException

from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.application.agency.commands.update.command import UpdateByName
from currency_convert.application.agency.queries.fetch_all.command import FetchAll
from currency_convert.application.primitives.command import CommandHandler
from currency_convert.application.primitives.query import QueryHandler
from currency_convert.domain.agency import valueobjects
from currency_convert.domain.agency.entities.agency import (
    AgencyNotFoundError,
    DuplicateAgencyError,
)
from currency_convert.domain.agency.entities.interface import UpdateStrategy
from currency_convert.domain.agency.valueobjects.currency import InvalidCurrencyError
from currency_convert.domain.primitives.valueobject import ValueObjectError
from currency_convert.presentation.converter import schemas
from currency_convert.presentation.converter.dependencies import (
    get_agency_update_strategy,
    get_all_query_handler,
    get_creation_handler,
    get_update_handler_by_name,
)

_logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/{agency_name}/create", status_code=201)
def api_create_agency(
    agency_name: str,
    base: str,
    url: str,
    country: str,
    handler: Annotated[
        CommandHandler[CreateAgency, schemas.Agency], Depends(get_creation_handler)
    ],
) -> schemas.Product[schemas.Agency]:
    cmd = CreateAgency(agency_name, base, url, country)
    try:
        result = handler.execute(cmd)
    except DuplicateAgencyError as exc:
        _logger.exception(exc)
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidCurrencyError as exc:
        _logger.exception(exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        _logger.critical("Unreachable code path.")
        raise HTTPException(status_code=500, detail="Internal server error.") from exc
    else:
        return schemas.Product(data=result)


@router.put("/{agency_name}/update", status_code=200)
def api_update(
    agency_name: str,
    strategy: Annotated[UpdateStrategy, Depends(get_agency_update_strategy)],
    handler: Annotated[
        CommandHandler[UpdateByName, None], Depends(get_update_handler_by_name)
    ],
) -> Literal[200]:
    cmd = UpdateByName(strategy, agency_name)
    try:
        handler.execute(cmd)
    except AgencyNotFoundError as exc:
        _logger.exception(exc)
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueObjectError as exc:
        _logger.critical(exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
    except Exception as e:
        _logger.critical("Unreachable code path.")
        raise HTTPException(status_code=500, detail="Internal server error.") from e
    else:
        return 200


@router.get("/{agency_name}/rates", response_model=schemas.Products[schemas.Rate])
def api_get_rates(
    agency_name: str,
    handler: Annotated[
        QueryHandler[FetchAll, tuple[valueobjects.Rate, ...]],
        Depends(get_all_query_handler),
    ],
) -> schemas.Products[schemas.Rate]:
    cmd = FetchAll(agency_name=agency_name)
    try:
        rates = handler.execute(cmd)
    except AgencyNotFoundError as exc:
        _logger.exception(exc)
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as e:
        _logger.critical("Unreachable code path.")
        raise HTTPException(status_code=500, detail="Internal server error.") from e
    else:
        return schemas.Products(data=[schemas.Rate(**asdict(rate)) for rate in rates])

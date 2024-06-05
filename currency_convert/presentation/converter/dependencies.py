from __future__ import annotations

from typing import Annotated, Iterator

import httpx
import xmltodict
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from currency_convert.application.agency.commands.create.handler import (
    CreateAgencyHandler,
)
from currency_convert.application.agency.commands.update.handler import (
    ByNameUpdateHandler,
)
from currency_convert.application.agency.queries.fetch_all.handler import (
    FetchAllHandler,
)
from currency_convert.application.agency.queries.fetch_one.handler import (
    FetchOneHandler,
)
from currency_convert.application.primitives.command import CommandHandler
from currency_convert.domain.agency.entities.interface import (
    AgencyRepository,
    UpdateStrategy,
)
from currency_convert.infrastructure.agency.repository import AgencyRepo
from currency_convert.infrastructure.update_strategies.ezb.real import (
    EZBUpdateStrategy,
    RequestHandler,
    XmlParser,
)
from currency_convert.presentation.config import get_app_settings

settings, _ = get_app_settings()

engine = create_engine(str(settings.DATABASE_URL))


def get_db() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_agency_repository(
    session: Annotated[Session, Depends(get_db)],
) -> AgencyRepository:
    return AgencyRepo(session)


def get_creation_handler(
    repo: Annotated[AgencyRepository, Depends(get_agency_repository)],
) -> CreateAgencyHandler:
    return CreateAgencyHandler(repo)


def get_update_handler_by_name(
    repo: Annotated[AgencyRepository, Depends(get_agency_repository)],
) -> ByNameUpdateHandler:
    return ByNameUpdateHandler(repo)


def get_one_query_handler(
    repo: Annotated[AgencyRepository, Depends(get_agency_repository)],
) -> FetchOneHandler:
    return FetchOneHandler(repo)


def get_all_query_handler(
    repo: Annotated[AgencyRepository, Depends(get_agency_repository)],
) -> FetchAllHandler:
    return FetchAllHandler(repo)


def get_xml_parser() -> XmlParser:
    return xmltodict  # type: ignore [return-value]


def get_request_handler() -> RequestHandler:
    return httpx.Client()  # type: ignore [return-value]


def get_agency_update_strategy(
    handler: Annotated[RequestHandler, Depends(get_request_handler)],
    parser: Annotated[XmlParser, Depends(get_xml_parser)],
) -> UpdateStrategy:
    return EZBUpdateStrategy(handler, parser)

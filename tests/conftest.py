from typing import Any, Callable, Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from currency_convert.application.agency.commands.create.command import CreateAgency
from currency_convert.application.agency.commands.create.handler import (
    CreateAgencyHandler,
)
from currency_convert.application.agency.commands.update.command import UpdatebyName
from currency_convert.application.agency.commands.update.handler import (
    ByNameUpdateHandler,
)
from currency_convert.infrastructure.agency.db import Base
from currency_convert.infrastructure.agency.repository import AgencyRepo
from currency_convert.infrastructure.update_strategies.ezb.memory import (
    MemoryUpdateStrategy,
)
from tests.data import INSERTS


@pytest.fixture()
def MemoryStrategy() -> MemoryUpdateStrategy:
    return MemoryUpdateStrategy(INSERTS)


@pytest.fixture
def MemoryEngine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def SessionFactory(MemoryEngine: Engine) -> Generator[sessionmaker[Session], Any, None]:
    yield sessionmaker(bind=MemoryEngine)


@pytest.fixture()
def EmptyAgencyRepository(SessionFactory: Callable[[], Session]) -> AgencyRepo:
    empty_memory_repo = AgencyRepo(SessionFactory())
    
    CreateAgencyHandler(empty_memory_repo).execute(
        CreateAgency(
            name="EZB",
            base="EUR",
            address="https://test.com",
            country="Test Country",
        )
    )

    return empty_memory_repo


@pytest.fixture()
def MemoryAgencyRepository(
    EmptyAgencyRepository: AgencyRepo, MemoryStrategy: MemoryUpdateStrategy
) -> AgencyRepo:
    cmd = UpdatebyName(MemoryStrategy, "EZB")
    handler = ByNameUpdateHandler(EmptyAgencyRepository)
    handler.execute(cmd)
    return EmptyAgencyRepository

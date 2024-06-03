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
from currency_convert.infrastructure.memory.agency.memory import Base, MemoryAgency
from currency_convert.infrastructure.update_strategies.ezb.memory import (
    EzbMemoryUpdateStrategy,
)
from tests.data import INSERTS


@pytest.fixture()
def MemoryStrategy() -> EzbMemoryUpdateStrategy:
    return EzbMemoryUpdateStrategy(INSERTS)


@pytest.fixture
def in_memory_sqlite_db() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(
    in_memory_sqlite_db: Engine,
) -> Generator[sessionmaker[Session], Any, None]:
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture()
def EmptyAgencyRepository(
    sqlite_session_factory: Callable[[], Session],
) -> MemoryAgency:
    empty_memory_repo = MemoryAgency(sqlite_session_factory())
    cmd = CreateAgency(
        name="EZB",
        base="EUR",
        address="https://test.com",
        country="Test Country",
    )
    handler = CreateAgencyHandler(empty_memory_repo)
    handler.execute(cmd)

    return empty_memory_repo


@pytest.fixture()
def MemoryAgencyRepository(
    EmptyAgencyRepository: MemoryAgency, MemoryStrategy: EzbMemoryUpdateStrategy
) -> MemoryAgency:
    cmd = UpdatebyName(MemoryStrategy, "EZB")
    handler = ByNameUpdateHandler(EmptyAgencyRepository)
    handler.execute(cmd)
    return EmptyAgencyRepository

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dependency_injector import containers, providers, wiring
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    async_scoped_session,
)

from notify_email.domain.email.interfaces.repository import (
    EmailReadRepositoryABC,
    EmailWriteRepositoryABC,
)

from notify_email.infra.email.repository import (
    SQLAlchemyEmailReadRepository,
    SQLAlchemyEmailWriteRepository,
    SQLAlchemyUnitOfWork,
)


class SQLAlchemyContainer(containers.DeclarativeContainer):
    config = providers.Configuration(
        yaml_files=["notify_email/infra/configs/main.yaml"]
    )
    db_async_url = providers.Object(
        f"postgresql+asyncpg://{config.pg.user}:{config.pg.password}"
        f"@{config.pg.host}:{config.pg.port}/{config.pg.db_name}"
    )

    engine = providers.Singleton(
        create_async_engine,
        db_async_url,
        echo=config.sql_debug,
    )
    session_maker = providers.Singleton(
        async_sessionmaker[AsyncSession],
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    # @classmethod
    # @asynccontextmanager
    # async def _async_db_session(
    #     cls, session_maker: async_sessionmaker[AsyncSession]
    # ) -> AsyncGenerator[AsyncSession, None]:
    #     async with session_maker() as db_session:
    #         yield db_session

    db_session = providers.Resource(session_maker)
    unit_of_work = providers.Factory(
        SQLAlchemyUnitOfWork,
        db_session,
        _register={
            EmailReadRepositoryABC: SQLAlchemyEmailReadRepository,
            EmailWriteRepositoryABC: SQLAlchemyEmailWriteRepository,
        },
    )


container = SQLAlchemyContainer()

container.config.pg.user.from_env("POSTGRES_USER", required=True)
container.config.pg.password.from_env("POSTGRES_PASSWORD", required=True)
container.config.pg.host.from_env("POSTGRES_HOST", required=True)
container.config.pg.port.from_env("POSTGRES_PORT", required=True, as_=int)
container.config.pg.db_name.from_env("POSTGRES_DBNAME", required=True)

container.config.sql_debug.from_env("SQL_DEBUG", default=True)

import logging
from typing import AsyncGenerator
from dependency_injector import containers, providers
import dotenv
from notify_channel.infra.dependencies.config import ConfigContainer
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from notify_channel.domain.email.interfaces.repository import (
    EmailReadRepositoryABC,
    EmailWriteRepositoryABC,
)

from notify_channel.infra.email.repository import (
    SQLAlchemyEmailReadRepository,
    SQLAlchemyEmailWriteRepository,
    SQLAlchemyUnitOfWork,
)


logger = logging.getLogger("app")


async def _unit_of_work(
    session_maker: async_sessionmaker[AsyncSession], repo_registry
) -> AsyncGenerator[SQLAlchemyUnitOfWork, None]:
    logger.debug("Создаем сессию")

    async with session_maker() as db_session:
        yield SQLAlchemyUnitOfWork(db_session, impl_classes=repo_registry)

    logger.debug("Убиваем сесиию")


class UnitOfWorkContainer(containers.DeclarativeContainer):
    session_maker = providers.Dependency()

    unit_of_work = providers.Resource(
        _unit_of_work,
        session_maker,
        repo_registry={
            EmailReadRepositoryABC: SQLAlchemyEmailReadRepository,
            EmailWriteRepositoryABC: SQLAlchemyEmailWriteRepository,
        },
    )


class SQLAlchemyContainer(containers.DeclarativeContainer):
    __self__ = providers.Self()

    config = providers.Configuration()
    db_async_url = providers.Singleton(
        lambda user, password, host, port, db_name: f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}",
        user=config.pg.user,
        password=config.pg.password,
        host=config.pg.host,
        port=config.pg.port,
        db_name=config.pg.db_name,
    )

    db_engine = providers.Singleton(
        create_async_engine,
        db_async_url,
        echo=config.sql_debug,
    )
    session_maker = providers.Singleton(
        async_sessionmaker[AsyncSession],
        db_engine,
        expire_on_commit=False,
        autocommit=False,
        class_=AsyncSession,
    )

    # UGLY: приходится для каждого unit_of_work создавать свой контейнер
    # так как Resource в dependency_injector это то же самое что и Singleton
    unit_of_work_cont = providers.Factory(
        UnitOfWorkContainer,
        session_maker=session_maker,
    )
    unit_of_work = providers.Factory(
        lambda self: self.unit_of_work_cont().unit_of_work(), __self__
    )

    @classmethod
    def set_config_from_env(cls, config: providers.Configuration):
        config.pg.user.from_env("POSTGRES_USER", required=True)
        config.pg.password.from_env("POSTGRES_PASSWORD", required=True)
        config.pg.host.from_env("POSTGRES_HOST", required=True)
        config.pg.port.from_env("POSTGRES_PORT", required=True, as_=int)
        config.pg.db_name.from_env("POSTGRES_DBNAME", required=True)

        config.sql_debug.from_env("SQL_DEBUG", default=True, as_=bool)


def get_sqlaclhemy_container() -> SQLAlchemyContainer:
    dotenv.load_dotenv()

    config_cont = ConfigContainer()
    SQLAlchemyContainer.set_config_from_env(config_cont.config)
    return SQLAlchemyContainer(config=config_cont.config)

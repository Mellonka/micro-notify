from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domains.message.domain.message_status import MessageStatus, Status
from src.domains.message.domain.message_status_unit_of_work import MessageStatusUnitOfWork
from src.domains.message.infra.sqlalchemy.message_status_repository import SQLAlchemyMessageStatusRepository
from src.domains.message.infra.sqlalchemy.metadata import session_factory

class SQLAlchemyGetMessageStatusUOW(MessageStatusUnitOfWork):

    def __init__(
        self,
        session_factory: async_sessionmaker = session_factory
    ):
        super().__init__()
        self.session_fac = session_factory

    async def __aenter__(self) -> Self:
        self.session: AsyncSession = self.session_fac()
        self.status_repo = SQLAlchemyMessageStatusRepository(self.session)
        return self
    
    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        self.session.expunge_all()
        await self.session.rollback()
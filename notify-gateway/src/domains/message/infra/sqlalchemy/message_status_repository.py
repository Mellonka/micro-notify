from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.domains.message.domain.message_status import MessageStatus
from src.domains.message.domain.message_status_repository import MessageStatusRepository
from src.domains.message.infra.sqlalchemy.mappers import (
    MessageStatusToDB,
    MessageStatusDBToDomain,
)
from src.domains.message.infra.sqlalchemy.models.message_status import MessageStatusDB


class SQLAlchemyMessageStatusRepository(MessageStatusRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def add(self, status: MessageStatus):
        self._session.add(MessageStatusToDB(status))

    async def update(self, status: MessageStatus):
        await self._session.execute(
            update(MessageStatusDB)
            .filter_by(id=status.id)
            .values(**status.model_dump(exclude={"id"}))
        )

    async def get_by_id(self, id) -> Optional[MessageStatus]:
        result = (
            await self._session.execute(select(MessageStatusDB).filter_by(id=id))
        ).scalar_one_or_none()
        if result is None:
            return None
        return MessageStatusDBToDomain(result)

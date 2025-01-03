from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from domain.message import Message
from domain.message_repository import MessageRepository
from mappers import MessageToDB, MessageDBToDomain
from models.message import MessageDB


class SQLAlchemyMessageRepository(MessageRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def add(self, msg: Message):
        self._session.add(MessageToDB(msg))
    
    async def update(self, msg: Message):
        await self._session.execute(
            update(MessageDB).filter_by(id=msg.id).values(**msg.model_dump(exclude={'id','external_id'}))
        )
    
    async def get_by_id(self, id) -> Optional[Message]:
        result = (
            await self._session.execute(
                select(MessageDB).filter_by(id=id)
        )).scalar_one_or_none
        if result is None:
            return None
        return MessageDBToDomain(result)
        
    
    async def get_by_external_id(self, id) -> Optional[Message]:
        result = (
            await self._session.execute(
                select(MessageDB).filter_by(external_id=id)
        )).scalar_one_or_none
        if result is None:
            return None
        return MessageDBToDomain(result)
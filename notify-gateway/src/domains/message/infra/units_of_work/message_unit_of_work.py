from typing import Self
from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domains.message.domain.message import Message
from src.domains.message.domain.message_status import MessageStatus, Status
from src.domains.message.domain.message_unit_of_work import CreateMessageUnitOfWork
from src.domains.message.infra.sqlalchemy.message_repository import (
    SQLAlchemyMessageRepository,
)
from src.domains.message.infra.sqlalchemy.message_status_repository import (
    SQLAlchemyMessageStatusRepository,
)
from src.domains.message.infra.aio_pika.publisher import RabbitMQPublisher
from src.domains.message.infra.sqlalchemy.metadata import session_factory


class SQLAlchemyMQCreateMessageUOW(CreateMessageUnitOfWork):
    def __init__(
        self,
        msg_broker: RabbitMQPublisher,
        session_factory: async_sessionmaker = session_factory,
    ):
        super().__init__()
        self.msg_broker = msg_broker
        self.session_fac = session_factory

    async def __aenter__(self) -> Self:
        self.session: AsyncSession = self.session_fac()
        self.message_repo = SQLAlchemyMessageRepository(self.session)
        self.status_repo = SQLAlchemyMessageStatusRepository(self.session)
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
        if self.msg is None:
            return
        await self.msg_broker.publish(self.msg)
        self.msg.pending = True
        await self.status_repo.add(
            MessageStatus(
                id=self.msg.id, status=Status.sending, updated_at=datetime.now()
            )
        )
        await self.message_repo.update(self.msg)
        await self.session.commit()

    async def add_mesg_to_commit(self, msg: Message):
        self.msg = msg

    async def rollback(self) -> None:
        self.msg = None
        self.session.expunge_all()
        await self.session.rollback()

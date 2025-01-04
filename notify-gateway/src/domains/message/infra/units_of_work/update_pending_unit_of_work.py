from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.domains.message.domain.update_pending_unit_of_work import (
    UpdatePendingUnitOfWork,
)
from src.domains.message.infra.sqlalchemy.message_repository import (
    SQLAlchemyMessageRepository,
)
from src.domains.message.infra.sqlalchemy.metadata import session_factory
from src.domains.message.domain.message import Message
from src.domains.message.infra.aio_pika.publisher import RabbitMQPublisher


class SQLAlchemyUpdatePendingUOW(UpdatePendingUnitOfWork):
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
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.session.close()

    async def commit(self) -> None:
        for msg in self.msgs:
            await self.msg_broker.publish(msg)
            msg.pending = True
            await self.message_repo.update(msg)
        await self.session.commit()

    async def add_mesg_to_update(self, msgs: list[Message]):
        self.msgs = msgs

    async def rollback(self) -> None:
        self.msg = None
        self.session.expunge_all()
        await self.session.rollback()

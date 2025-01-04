from abc import ABC, abstractmethod

from src.domains.message.domain.message import Message
from src.domains.message.domain.unit_of_work import UnitOfWork
from src.domains.message.domain.message_repository import MessageRepository
from src.domains.message.domain.message_status_repository import MessageStatusRepository

class CreateMessageUnitOfWork(UnitOfWork, ABC):
    message_repo: MessageRepository
    status_repo: MessageStatusRepository

    @abstractmethod
    async def add_mesg_to_commit(self, msg: Message):
        self.msg = msg
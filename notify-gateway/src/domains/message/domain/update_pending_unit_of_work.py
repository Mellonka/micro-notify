from abc import ABC, abstractmethod

from src.domains.message.domain.message import Message
from src.domains.message.domain.unit_of_work import UnitOfWork
from src.domains.message.domain.message_repository import MessageRepository

class UpdatePendingUnitOfWork(UnitOfWork, ABC):
    message_repo: MessageRepository


    @abstractmethod
    async def add_mesg_to_update(self, msgs: list[Message]):
        self.msgs = msgs

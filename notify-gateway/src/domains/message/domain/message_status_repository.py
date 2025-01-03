from abc import ABC, abstractmethod
from typing import Optional

from domain.message_status import MessageStatus


class MessageStatusRepository(ABC):
    @abstractmethod
    async def add(self, msg: MessageStatus):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, msg: MessageStatus):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id) -> Optional[MessageStatus]:
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Optional

from domain.message import Message


class MessageRepository(ABC):
    @abstractmethod
    async def add(self, msg: Message):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, msg: Message):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id) -> Optional[Message]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_external_id(self, id) -> Optional[Message]:
        raise NotImplementedError
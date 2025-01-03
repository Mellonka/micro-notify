from abc import ABC

from unit_of_work import UnitOfWork
from message_repository import MessageRepository

class MessageUnitOfWork(UnitOfWork, ABC):
    message_repo: MessageRepository
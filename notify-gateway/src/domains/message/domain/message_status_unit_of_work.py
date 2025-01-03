from abc import ABC

from unit_of_work import UnitOfWork
from message_status_repository import MessageStatusRepository

class MessageStatusUnitOfWork(UnitOfWork, ABC):
    status_repo: MessageStatusRepository
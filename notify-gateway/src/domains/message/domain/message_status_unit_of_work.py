from abc import ABC

from src.domains.message.domain.unit_of_work import UnitOfWork
from src.domains.message.domain.message_status_repository import MessageStatusRepository

class MessageStatusUnitOfWork(UnitOfWork, ABC):
    status_repo: MessageStatusRepository
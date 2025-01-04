from abc import ABC, abstractmethod

from ..models import Email, EmailBaseEvent

from notify_shared.storage import ReadRepositoryABC, WriteRepositoryABC


class EmailReadRepositoryABC(ReadRepositoryABC, ABC):
    @abstractmethod
    async def load_by_conflict(self, external_id: str) -> Email | None:
        raise NotImplementedError

    @abstractmethod
    async def exist_by_conflict(self, external_id: str) -> bool:
        raise NotImplementedError


class EmailWriteRepositoryABC(WriteRepositoryABC, ABC):
    @abstractmethod
    async def insert(self, email: Email) -> None:
        raise NotImplementedError

    @abstractmethod
    async def insert_domain_event(self, event: EmailBaseEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, email: Email) -> None:
        raise NotImplementedError

from ..models import Mail

from notify_shared.storage import ReadRepositoryABC, WriteRepositoryABC


class MailReadRepositoryABC(ReadRepositoryABC):
    async def load_by_conflict(self, sender: str, external_id: str) -> Mail:
        raise NotImplementedError

    async def exist_by_conflict(self, sender: str, external_id: str) -> bool:
        raise NotImplementedError


class MailWriteRepositoryABC(WriteRepositoryABC):
    def add(self, mail: Mail):
        raise NotImplementedError

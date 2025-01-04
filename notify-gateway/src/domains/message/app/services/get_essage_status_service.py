from uuid import UUID
from src.domains.message.domain.message_status_unit_of_work import (
    MessageStatusUnitOfWork,
)
from src.domains.message.domain.message_status import MessageStatus


class GetMessageStatusService:
    def __init__(self, status_uow: MessageStatusUnitOfWork):
        self.status_uow = status_uow

    async def get_status(self, id: UUID) -> MessageStatus | None:
        async with self.status_uow as uow:
            result = await uow.status_repo.get_by_id(id)
            return result

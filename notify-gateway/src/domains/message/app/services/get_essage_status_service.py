from uuid import UUID
from domain.message_status import MessageStatus
from domain.message_status_unit_of_work import MessageStatusUnitOfWork

class CreateMessageService:
    def __init__(self, status_uow: MessageStatusUnitOfWork):
        self.status_uow = status_uow

    async def get_status(self, status: MessageStatus) -> str:
        async with self.status_uow as uow:
            result = await uow.status_repo.get_by_id(status.id)
            if result is not None:
                return result.status
            return "Not found"
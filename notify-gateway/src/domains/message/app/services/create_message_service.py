from uuid import UUID
from domain.message import Message
from domain.message_unit_of_work import MessageUnitOfWork

class CreateMessageService:
    def __init__(self, msg_uow: MessageUnitOfWork):
        self.msg_uow = msg_uow

    async def create_msg(self, msg: Message) -> UUID:
        async with self.msg_uow as uow:
            result = await uow.message_repo.get_by_external_id(msg.external_id)
            if result is not None:
                return result.id
            await uow.message_repo.add(msg)
            await uow.commit()
            return msg.id
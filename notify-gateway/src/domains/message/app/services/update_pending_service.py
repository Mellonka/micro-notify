from src.domains.message.domain.update_pending_unit_of_work import UpdatePendingUnitOfWork

class UpdatePendingService:
    def __init__(self, update_uow: UpdatePendingUnitOfWork):
        self.update_uow = update_uow

    async def update_pending(self) -> int:
        rows = 0
        async with self.update_uow as uow:
            to_update = await uow.message_repo.get_not_pending(5)
            rows = len(to_update)
            await uow.add_mesg_to_update(to_update)
            await uow.commit()
        return rows
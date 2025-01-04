import asyncio
from src.domains.message.app.services.update_pending_service import UpdatePendingService
from src.domains.message.infra.units_of_work.update_pending_unit_of_work import (
    SQLAlchemyUpdatePendingUOW,
)
from src.domains.message.infra.aio_pika.publisher import RabbitMQPublisher


async def main():
    rabbitmq = RabbitMQPublisher()
    await rabbitmq.connect()
    update_pending_uow = SQLAlchemyUpdatePendingUOW(msg_broker=rabbitmq)
    update_pending_service = UpdatePendingService(update_pending_uow)
    while True:
        count = await update_pending_service.update_pending()
        if count == 0:
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())

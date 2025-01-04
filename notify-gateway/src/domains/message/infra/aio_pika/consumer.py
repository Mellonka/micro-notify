import logging
import json

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from src.domains.message.domain.message_status import MessageStatus
from src.config import RABBITMQ_URL, EMAIL_STATUS_QUEUE
from src.domains.message.infra.units_of_work.message_status_unit_of_work import (
    SQLAlchemyGetMessageStatusUOW,
)

logger = logging.getLogger(__name__)


class RabbitMQConsumer:
    async def connect(self):
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()

    async def handle_message(
        self,
        message: AbstractIncomingMessage,
        unit_of_work: SQLAlchemyGetMessageStatusUOW,
    ) -> None:
        data = json.loads(message.body)
        await unit_of_work.status_repo.update(
            MessageStatus(
                id=data["event_data"]["external_id"],
                updated_at=data["timestamp"],
                status=data["event_data"]["status"],
            )
        )
        await unit_of_work.commit()
        await message.ack()

        logger.info("Обработали сообщение: %s", message.body.decode())

    async def run(self):
        queue = await self.channel.declare_queue(name=EMAIL_STATUS_QUEUE, durable=True)
        async with SQLAlchemyGetMessageStatusUOW() as unit_of_work:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await self.handle_message(message, unit_of_work)

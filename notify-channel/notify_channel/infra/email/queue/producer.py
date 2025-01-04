from dataclasses import dataclass

import aio_pika
from pydantic import BaseModel


@dataclass
class RabbitMQProducer:
    queue: aio_pika.abc.AbstractRobustQueue

    async def publish(self, message: BaseModel) -> None:
        await self.queue.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=self.queue.name,
        )

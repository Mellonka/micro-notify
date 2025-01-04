import aio_pika

from src.domains.message.domain.message import Message
from src.config import RABBITMQ_URL, queues
from src.domains.message.infra.aio_pika.mappers import mappers


class RabbitMQPublisher:
    async def connect(self):
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()

    async def publish(self, msg: Message):
        body = mappers[msg.type](msg)
        await self.channel.declare_queue(queues[msg.type], durable=True)
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=body.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT,),
            routing_key=queues[msg.type],
        )
import asyncio
from src.domains.message.infra.aio_pika.consumer import RabbitMQConsumer


async def main():
    rabbitmq = RabbitMQConsumer()
    await rabbitmq.connect()
    await rabbitmq.run()


if __name__ == "__main__":
    asyncio.run(main())

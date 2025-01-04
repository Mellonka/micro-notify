import logging
from dataclasses import dataclass
from typing import AsyncIterable

from pydantic import ValidationError
from aio_pika.abc import (
    AbstractRobustQueue,
    AbstractIncomingMessage,
)

from notify_channel.application.commands.send_email import (
    SendEmailCommand,
    SendEmailHandler,
    AlreadySentError,
)


logger = logging.getLogger("app")


@dataclass
class RabbitMQConsumer:
    queue: AbstractRobustQueue
    handler: SendEmailHandler

    async def handle_message(self, message: AbstractIncomingMessage) -> None:
        try:
            command = SendEmailCommand.model_validate_json(message.body)
            await self.handler.handle(command)
        except ValidationError as exc:
            logger.exception(
                "Не валидное сообщение: %s", message.body.decode(), exc_info=exc,
            )
            await message.reject()
        except AlreadySentError:
            logger.info("Уже отправленое сообщение: %s", message.body.decode())
            await message.reject()
        except Exception as exc:
            logger.exception("Неожиданная ошибка", exc_info=exc)
            await message.nack()
        else:
            logger.info("Обработали сообщение")
            await message.ack()

    async def iterator(self) -> AsyncIterable[AbstractIncomingMessage]:
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                yield message

    async def run(self):
        async for message in self.iterator():
            await self.handle_message(message)

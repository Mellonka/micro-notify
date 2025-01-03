import logging
import datetime as dt
from dataclasses import dataclass
from typing import AsyncIterable

from pydantic import ValidationError
from aio_pika.abc import (
    AbstractRobustQueue,
    AbstractIncomingMessage,
)

from notify_email.application.commands.send_email import (
    SendEmailCommand,
    SendEmailHandler,
    AlreadySentError,
)


@dataclass
class RabbitMQConsumer:
    queue: AbstractRobustQueue
    handler: SendEmailHandler
    logger: logging.Logger

    async def handle_message(self, message: AbstractIncomingMessage) -> None:
        try:
            command = SendEmailCommand.model_validate_json(message.body)
            await self.handler.handle(command)
        except ValidationError as exc:
            self.logger.error("Не валидное сообщение %s", exc)
            await message.reject()
        except AlreadySentError as exc:
            self.logger.error("Уже отправленое сообщение %s", exc)
            await message.reject()
        except Exception as exc:
            self.logger.error("Неожиданная ошибка %s", exc)
            await message.nack()
        else:
            self.logger.error("Обработали сообщение")
            await message.ack()

    async def iterator(self) -> AsyncIterable[AbstractIncomingMessage]:
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                yield message

    async def run(self):
        async for message in self.iterator():
            await self.handle_message(message)

from dataclasses import dataclass
import aiosmtplib
from email.message import EmailMessage

from notify_channel.application.services.email import EmailServiceABC, SendFailedError
from notify_channel.domain.email.models import Email

import logging

from notify_channel.domain.email.models.events import EmailBaseEvent
from notify_channel.infra.email.queue.producer import RabbitMQProducer

logger = logging.getLogger("app")


@dataclass
class EmailService(EmailServiceABC):
    smtp: aiosmtplib.SMTP
    smtp_username: str

    event_producer: RabbitMQProducer

    async def send(self, email: Email) -> None:
        message = EmailMessage()
        message["From"] = email.sender
        message["To"] = ", ".join(email.receivers)
        message["Subject"] = email.subject
        message.set_content(email.content)

        try:
            response = await self.smtp.send_message(message)
            logger.info("Получили ответ: %s", response)
        except aiosmtplib.errors.SMTPException:
            raise SendFailedError

    async def publish_event(self, event: EmailBaseEvent) -> None:
        await self.event_producer.publish(event)

        logger.info('Отправили ивент: %s', event.model_dump_json())

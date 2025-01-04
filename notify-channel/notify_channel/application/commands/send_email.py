from dataclasses import dataclass
from functools import cached_property
import datetime as dt
from uuid import uuid4

from notify_channel.application.services.email import (
    SendFailedError,
    EmailServiceABC,
)
from notify_channel.domain.email.models import (
    Email,
    EmailStatus,
    EmailSendingFailedEvent,
    EmailSendingSuccessEvent,
)
from notify_channel.domain.email.interfaces.repository import (
    EmailReadRepositoryABC,
    EmailWriteRepositoryABC,
)

from notify_shared import Command, CommandHandler, UnitOfWorkABC
from notify_shared.utils import now

from pydantic import EmailStr, Field

import logging

logger = logging.getLogger("app")


class AlreadySentError(Exception):
    pass


class RetryCommandError(Exception):
    pass


class SendEmailCommand(Command):
    external_id: str
    created_at: dt.datetime = Field(default_factory=now)

    sender: str
    subject: str | None = None
    content: str
    receivers: list[EmailStr]


@dataclass
class SendEmailHandler(CommandHandler[SendEmailCommand, None]):
    email_service: EmailServiceABC
    unit_of_work: UnitOfWorkABC

    @cached_property
    def email_read_repo(self) -> EmailReadRepositoryABC:
        return self.unit_of_work.get_repository(EmailReadRepositoryABC)

    @cached_property
    def email_write_repo(self) -> EmailWriteRepositoryABC:
        return self.unit_of_work.get_repository(EmailWriteRepositoryABC)

    async def handle(self, request: SendEmailCommand) -> None:
        email = await self.email_read_repo.load_by_conflict(request.external_id)

        if not email:
            email = Email(
                id=uuid4(),
                external_id=request.external_id,
                created_at=request.created_at,
                status=EmailStatus.sending,
                sender=request.sender,
                subject=request.subject,
                content=request.content,
                receivers=request.receivers,
            )
            await self.email_write_repo.insert(email)
            await self.unit_of_work.commit()
        elif email.status == EmailStatus.sent:
            raise AlreadySentError

        try:
            await self.email_service.send(email)
        except SendFailedError:
            email.status = EmailStatus.retrying
            event = EmailSendingFailedEvent(email_id=email.id)
        else:
            email.status = EmailStatus.sent
            event = EmailSendingSuccessEvent(email_id=email.id)
            logger.info("Отправили email с external_id = %s", email.external_id)

        await self.email_service.publish_event(event)

        await self.email_write_repo.insert_domain_event(event)
        await self.email_write_repo.update_status(email)
        await self.unit_of_work.commit()

        if email.status == EmailStatus.retrying:
            raise RetryCommandError

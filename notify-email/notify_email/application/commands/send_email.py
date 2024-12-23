import datetime as dt
from uuid import uuid4

from notify_email.application.services.smtp_email import (
    SendFailedError,
    SmtpEmailServiceABC,
)
from notify_email.domain.mail.models import Mail, MailStatus
from notify_email.domain.mail.interfaces.repository import (
    MailReadRepositoryABC,
    MailWriteRepositoryABC,
)

from notify_shared import Command, CommandHandler, UnitOfWorkABC

from pydantic import EmailStr


class AlreadySentError(Exception):
    pass


class SendEmailCommand(Command):
    external_id: str

    subject: str | None
    text: str
    sender: str
    receiver: list[EmailStr]


class SendEmailHandler(CommandHandler[SendEmailCommand, None]):
    unit_of_work: UnitOfWorkABC
    mail_read_repo: MailReadRepositoryABC
    mail_write_repo: MailWriteRepositoryABC
    smtp_email_service: SmtpEmailServiceABC

    async def handle(self, request: SendEmailCommand) -> None:
        if not self.mail_read_repo.exist_by_conflict(
            request.sender, request.external_id
        ):
            mail = Mail(
                id=uuid4(),
                external_id=request.external_id,
                created_at=dt.datetime.now(),
                subject=request.subject,
                text=request.text,
                sender=request.sender,
                receiver=request.receiver,
                status=MailStatus.sending,
            )

            self.mail_write_repo.add(mail)
            await self.unit_of_work.commit()
        else:
            mail = await self.mail_read_repo.load_by_conflict(
                request.sender, request.external_id
            )
            if mail.status == MailStatus.sended:
                raise AlreadySentError

        try:
            await self.smtp_email_service.send(mail)
        except SendFailedError:
            mail.status = MailStatus.retrying
        else:
            mail.status = MailStatus.sended

        mail.last_send_at = dt.datetime.now()
        await self.unit_of_work.commit()

from dataclasses import dataclass
import aiosmtplib
from email.message import EmailMessage

from notify_email.application.services.email import EmailServiceABC
from notify_email.domain.email.models import Email


@dataclass
class SmtpEmailService(EmailServiceABC):
    smtp: aiosmtplib.SMTP
    username: str

    async def send(self, email: Email) -> None:
        message = EmailMessage()
        message["From"] = self.username
        message["To"] = email.receivers
        message["Subject"] = email.subject
        message.set_content(email.content)
        await self.smtp.send_message(message)

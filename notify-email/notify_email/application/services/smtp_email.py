from notify_email.domain.mail.models import Mail


class SendFailedError(Exception):
    pass


class SmtpEmailServiceABC:
    async def send(self, mail: Mail) -> None:
        raise NotImplementedError

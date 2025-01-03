from abc import ABC, abstractmethod

from notify_email.domain.email.models import Email


class SendFailedError(Exception):
    pass


class EmailServiceABC(ABC):
    @abstractmethod
    async def send(self, email: Email) -> None:
        raise NotImplementedError

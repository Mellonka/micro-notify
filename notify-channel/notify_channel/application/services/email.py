from abc import ABC, abstractmethod

from notify_channel.domain.email.models import Email, EmailBaseEvent


class SendFailedError(Exception):
    pass


class EmailServiceABC(ABC):
    @abstractmethod
    async def send(self, email: Email) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish_event(self, event: EmailBaseEvent) -> None:
        raise NotImplementedError

from uuid import UUID

from notify_shared import BaseDomainEvent


class EmailBaseEvent(BaseDomainEvent):
    email_id: UUID
    event: str


class EmailSendingSuccessEvent(EmailBaseEvent):
    event: str = "sending_success"


class EmailSendingFailedEvent(EmailBaseEvent):
    event: str = "sending_failed"

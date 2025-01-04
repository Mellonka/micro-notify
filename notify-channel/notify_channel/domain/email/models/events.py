from uuid import UUID

from notify_shared import BaseDomainEvent


class EmailBaseEvent(BaseDomainEvent):
    event: str
    email_id: UUID | None = None
    event_data: dict | None = None


class EmailParsingFailedEvent(EmailBaseEvent):
    event: str = "parsing_failed"


class EmailSendingSuccessEvent(EmailBaseEvent):
    event: str = "sending_success"


class EmailSendingFailedEvent(EmailBaseEvent):
    event: str = "sending_failed"

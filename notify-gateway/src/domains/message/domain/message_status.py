from enum import StrEnum
from uuid import UUID
from datetime import datetime

from src.domains.message.domain.base import AggregateRoot, Entity


class Status(StrEnum):
    sending = "sending"
    retrying = "retrying"
    sent = "sent"
    failed = "failed"


class MessageStatus(AggregateRoot, Entity[UUID]):
    status: Status
    updated_at: datetime

import datetime as dt
from uuid import UUID
from enum import StrEnum, auto

from notify_shared import AggregateRoot, Entity
from pydantic import EmailStr


class EmailStatus(StrEnum):
    sending = auto()
    sent = auto()
    retrying = auto()


class Email(AggregateRoot, Entity[UUID]):
    status: EmailStatus
    created_at: dt.datetime

    external_id: str

    sender: str
    subject: str | None
    content: str
    receivers: list[EmailStr]

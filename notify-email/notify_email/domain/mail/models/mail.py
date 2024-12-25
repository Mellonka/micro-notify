import datetime as dt
from uuid import UUID
from enum import StrEnum, auto

from notify_shared import AggregateRoot, Entity
from pydantic import EmailStr


class MailStatus(StrEnum):
    sending = auto()
    retrying = auto()
    sended = auto()


class Mail(AggregateRoot, Entity[UUID]):
    external_id: str
    status: MailStatus
    created_at: dt.datetime
    last_send_at: dt.datetime | None = None

    subject: str | None
    text: str
    sender: str
    receiver: list[EmailStr]

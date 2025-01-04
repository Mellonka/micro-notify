from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import model_validator, validate_email
import phonenumbers

from src.domains.message.domain.base import AggregateRoot, Entity


class MessageType(StrEnum):
    telegram = "telegram"
    sms = "sms"
    email = "email"


class Message(AggregateRoot, Entity[UUID]):
    external_id: str
    type: MessageType
    reciver: str
    sender: str
    text: str
    pending: bool
    meta: dict

    @model_validator(mode="after")
    def validate_reciver(self) -> Self:
        if self.type == MessageType.email:
            validate_email(self.reciver)
        if self.type == MessageType.sms:
            parsed_number = phonenumbers.parse(self.reciver)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError
        return self

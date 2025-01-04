from pydantic import BaseModel
from src.domains.message.domain.message import MessageType


class CreateMessage(BaseModel):
    external_id: str
    type: MessageType
    reciver: str
    sender: str
    text: str
    meta: dict

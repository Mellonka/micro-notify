from pydantic import BaseModel, EmailStr
from src.domains.message.domain.message import Message


class Email(BaseModel):
    external_id: str

    sender: str
    subject: str | None = None
    content: str
    receivers: list[EmailStr]


def MessageToEmail(msg: Message) -> str:
    email = Email(
        external_id=str(msg.id),
        sender=msg.sender,
        subject=None,
        content=msg.text,
        receivers=[msg.reciver],
    )
    return email.model_dump_json()
    return (
        "{"
        + f'"external_id": "{msg.id}", "sender": "{msg.sender}", "subject": null, "content": {msg.text}, "receivers" :["{msg.reciver}"]'
        + "}"
    )


mappers = {
    "email": MessageToEmail,
}

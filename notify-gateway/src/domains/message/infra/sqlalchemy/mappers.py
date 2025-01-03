from domain.message import Message
from models.message import MessageDB
from domain.message_status import MessageStatus
from models.message_status import MessageStatusDB


def MessageToDB(msg: Message) -> MessageDB:
    return MessageDB(
        id=msg.id,
        external_id=msg.external_id,
        type=msg.type,
        reciver=msg.reciver,
        sender=msg.sender,
        pending=msg.pending,
        text=msg.text,
        meta=msg.meta
    )


def MessageDBToDomain(msg: MessageDB) -> Message:
    return Message(
        id=msg.id,
        external_id=msg.external_id,
        type=msg.type,
        reciver=msg.reciver,
        sender=msg.sender,
        pending=msg.pending,
        text=msg.text,
        meta=msg.meta
    )


def MessageStatusToDB(status: MessageStatus) -> MessageStatusDB:
    return MessageStatusDB(
        id=status.id,
        status=status.status,
        updated_at=status.updated_at
    )


def MessageStatusDBToDomain(status: MessageStatusDB) -> MessageStatus:
    return MessageStatus(
        id=status.id,
        status=status.status,
        updated_at=status.updated_at
    )
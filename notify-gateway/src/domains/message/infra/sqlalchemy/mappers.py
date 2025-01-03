from domain.message import Message
from models.message import MessageDB

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
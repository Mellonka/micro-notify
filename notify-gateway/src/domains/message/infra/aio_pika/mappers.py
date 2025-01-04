from src.domains.message.domain.message import Message


def MessageToEmail(msg: Message) -> str:
    return '{' + f'"external_id":"{msg.id}","sender":{msg.sender},"subject":{msg.meta["subject"]},"content":{msg.text},"receivers":[{msg.reciver}]' + '}'


mappers = {
    "email": MessageToEmail,
}
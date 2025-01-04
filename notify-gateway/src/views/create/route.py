from uuid import UUID, uuid4
from fastapi import APIRouter, Request

from src.views.create.schemas import CreateMessage
from src.domains.message.domain.message import Message
from src.domains.message.app.services.create_message_service import CreateMessageService

create_router = APIRouter(prefix="/create")


@create_router.post("/")
async def create_msg(msg: CreateMessage, request: Request) -> UUID:
    service: CreateMessageService = request.app.extra["create_service"]

    id = await service.create_msg(
        Message(
            id=uuid4(),
            external_id=msg.external_id,
            type=msg.type,
            reciver=msg.reciver,
            sender=msg.sender,
            text=msg.text,
            pending=False,
            meta=msg.meta,
        )
    )
    return id

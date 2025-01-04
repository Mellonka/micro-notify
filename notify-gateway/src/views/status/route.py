from uuid import UUID
from fastapi import APIRouter, Request, Query
import datetime as dt

from src.domains.message.app.services.get_essage_status_service import (
    GetMessageStatusService,
)
from src.domains.message.domain.message_status import MessageStatus, Status


status_router = APIRouter(prefix="/status")


@status_router.get("/")
async def create_msg(request: Request, id: UUID = Query()) -> MessageStatus:
    service: GetMessageStatusService = request.app.extra["status_service"]
    status = await service.get_status(id=id)
    if not status:
        status = MessageStatus(
            id=id, status=Status.sending, updated_at=dt.datetime.now(tz=dt.UTC)
        )

    return status

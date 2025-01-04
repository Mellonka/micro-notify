from uuid import UUID
from fastapi import APIRouter, Request, Query

from src.domains.message.app.services.get_essage_status_service import (
    GetMessageStatusService,
)


status_router = APIRouter(prefix="/status")


@status_router.get("/")
async def create_msg(request: Request, id: UUID = Query()) -> str:
    service: GetMessageStatusService = request.app.extra["status_service"]

    status = await service.get_status(id=id)
    return status

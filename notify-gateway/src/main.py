from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.domains.message.app.services.create_message_service import CreateMessageService
from src.domains.message.infra.units_of_work.message_unit_of_work import (
    SQLAlchemyMQCreateMessageUOW,
)
from src.domains.message.app.services.get_essage_status_service import (
    GetMessageStatusService,
)
from src.domains.message.infra.units_of_work.message_status_unit_of_work import (
    SQLAlchemyGetMessageStatusUOW,
)
from src.domains.message.infra.aio_pika.publisher import RabbitMQPublisher

from src.views.create.route import create_router
from src.views.status.route import status_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.extra["rabbitmq"] = RabbitMQPublisher()
    await app.extra["rabbitmq"].connect()
    app.extra["create_msg_uow"] = SQLAlchemyMQCreateMessageUOW(
        msg_broker=app.extra["rabbitmq"]
    )
    app.extra["create_service"] = CreateMessageService(app.extra["create_msg_uow"])
    app.extra["status_uow"] = SQLAlchemyGetMessageStatusUOW()
    app.extra["status_service"] = GetMessageStatusService(app.extra["status_uow"])

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(create_router)
app.include_router(status_router)

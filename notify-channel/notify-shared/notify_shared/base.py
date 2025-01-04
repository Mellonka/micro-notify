import datetime as dt

from pydantic import BaseModel, Field

from notify_shared.utils import now


class BaseDomainEvent(BaseModel):
    timestamp: dt.datetime = Field(default_factory=now)
    event: str


class AggregateRoot(BaseModel):
    pass


class BaseEntity(BaseModel):
    pass


class Entity[TKey](BaseEntity):
    id: TKey


class HandleBase[TRequest, TResult]:
    async def handle(self, request: TRequest) -> TResult:
        raise NotImplementedError

from pydantic import BaseModel


class AggregateRoot(BaseModel):
    pass


class BaseEntity(BaseModel):
    pass


class Entity[TKey](BaseEntity):
    id: TKey


class HandleBase[TRequest, TResult](BaseModel):
    async def handle(self, request: TRequest) -> TResult:
        raise NotImplementedError

from pydantic import BaseModel


class AggregateRoot(BaseModel):
    pass


class BaseEntity(BaseModel):
    pass


class Entity[TKey](BaseEntity):
    id: TKey

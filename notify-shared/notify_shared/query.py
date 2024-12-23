from .base import HandleBase

from pydantic import BaseModel


class Query(BaseModel):
    pass


class QueryHandler[TQuery: Query, TResult](HandleBase[TQuery, TResult]):
    pass

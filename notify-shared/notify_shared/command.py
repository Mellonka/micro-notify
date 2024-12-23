from .base import HandleBase

from pydantic import BaseModel


class Command(BaseModel):
    pass


class CommandHandler[TCommand: Command, TResult](HandleBase[TCommand, TResult]):
    pass

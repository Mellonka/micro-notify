from __future__ import annotations
from typing import Iterable


class Cursor[T]:
    items: list[T]

    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError


class ReadRepositoryABC:
    unit_of_work: UnitOfWorkABC


class WriteRepositoryABC:
    unit_of_work: UnitOfWorkABC


class UnitOfWorkABC:
    async def begin(self) -> None:
        raise NotImplementedError

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError

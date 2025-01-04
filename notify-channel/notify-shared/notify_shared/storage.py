from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Cursor[T]:
    items: list[T]

    def __iter__(self) -> Iterable[T]:
        raise NotImplementedError


type RepositoryABC = ReadRepositoryABC | WriteRepositoryABC


@dataclass(eq=False)
class ReadRepositoryABC(ABC):
    unit_of_work: UnitOfWorkABC


@dataclass(eq=False)
class WriteRepositoryABC(ABC):
    unit_of_work: UnitOfWorkABC


@dataclass(eq=False)
class UnitOfWorkABC(ABC):
    @abstractmethod
    async def begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_repository[T: RepositoryABC](self, base_cls: type[T]) -> T:
        raise NotImplementedError

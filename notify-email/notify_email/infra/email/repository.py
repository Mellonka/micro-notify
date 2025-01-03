from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from uuid import UUID

from sqlalchemy import select, exists, DateTime, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from notify_shared.storage import UnitOfWorkABC, RepositoryABC

from notify_email.domain.email.interfaces.repository import (
    EmailReadRepositoryABC,
    EmailWriteRepositoryABC,
)
from notify_email.domain.email.models import Email


@dataclass
class SQLAlchemyUnitOfWork(UnitOfWorkABC):
    db_session: AsyncSession

    _register: dict[type[RepositoryABC], type[SQLAlchemyRepository]]

    async def begin(self) -> None:
        await self.db_session.begin()

    async def commit(self) -> None:
        await self.db_session.begin()

    async def rollback(self) -> None:
        await self.db_session.rollback()

    def get_repository(self, base_cls: type[RepositoryABC]) -> SQLAlchemyRepository:
        if base_cls not in self._register:
            raise Exception("Not registered repository")

        impl_cls = self._register[base_cls]
        return impl_cls(unit_of_work=self, db_session=self.db_session)


class SQLAlchemyEmail(DeclarativeBase):
    __tablename__ = "emails"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))

    sender: Mapped[str] = mapped_column()
    subject: Mapped[str | None] = mapped_column()
    content: Mapped[str] = mapped_column()
    receivers: Mapped[list[str]] = mapped_column()

    __table_args__ = (UniqueConstraint(sender, external_id),)


type SQLAlchemyRepository = SQLAlchemyEmailReadRepository | SQLAlchemyEmailWriteRepository


@dataclass
class SQLAlchemyEmailReadRepository(EmailReadRepositoryABC):
    db_session: AsyncSession

    async def load_by_conflict(self, external_id: str) -> Email | None:
        email = await self.db_session.scalar(
            select(SQLAlchemyEmail).where(SQLAlchemyEmail.external_id == external_id)
        )
        return Email.model_validate(email, from_attributes=True)

    async def exist_by_conflict(self, external_id: str) -> bool:
        return bool(
            await self.db_session.scalar(
                exists(SQLAlchemyEmail)
                .where(SQLAlchemyEmail.external_id == external_id)
                .select()
            )
        )


@dataclass
class SQLAlchemyEmailWriteRepository(EmailWriteRepositoryABC):
    db_session: AsyncSession

    def add(self, email: Email) -> None:
        return self.db_session.add(email)  # <--- все нахер взорвется????

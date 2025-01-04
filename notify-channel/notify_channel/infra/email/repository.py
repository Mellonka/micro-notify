from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
from uuid import UUID

from notify_channel.domain.email.models.events import EmailBaseEvent
from notify_channel.infra.shared.sqlalchemy import SQLAlchemyBase
from sqlalchemy import (
    ForeignKey,
    insert,
    select,
    exists,
    update,
    DateTime,
    String,
    Index,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from notify_shared.storage import UnitOfWorkABC, RepositoryABC

from notify_channel.domain.email.interfaces.repository import (
    EmailReadRepositoryABC,
    EmailWriteRepositoryABC,
)
from notify_channel.domain.email.models import Email


@dataclass
class SQLAlchemyUnitOfWork(UnitOfWorkABC):
    db_session: AsyncSession
    impl_classes: dict[type[RepositoryABC], type[SQLAlchemyRepository]]

    async def begin(self) -> None:
        await self.db_session.begin()

    async def commit(self) -> None:
        await self.db_session.commit()

    async def rollback(self) -> None:
        await self.db_session.rollback()

    def get_repository(self, base_cls: type[RepositoryABC]) -> SQLAlchemyRepository:
        if base_cls not in self.impl_classes:
            raise Exception("Not registered repository")

        impl_cls = self.impl_classes[base_cls]
        return impl_cls(unit_of_work=self, db_session=self.db_session)


class SQLAlchemyEmail(SQLAlchemyBase):
    __tablename__ = "emails"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(length=100), unique=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str]

    sender: Mapped[str]
    subject: Mapped[str | None]
    content: Mapped[str]
    receivers: Mapped[list[str]] = mapped_column(
        postgresql.ARRAY(String, as_tuple=True)
    )


class SQLAlchemyEmailEvent(SQLAlchemyBase):
    __tablename__ = "email_events"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    email_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("emails.id"), nullable=True
    )
    timestamp: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    event: Mapped[str] = mapped_column()
    event_data: Mapped[dict | None] = mapped_column(postgresql.JSONB())

    __table_args__ = (
        Index(
            "email_events_by_email_idx",
            email_id,
            id,
            postgresql_where=email_id.is_not(None),
        ),
        Index("email_events_by_event_idx", event, timestamp, id),
    )


type SQLAlchemyRepository = SQLAlchemyEmailReadRepository | SQLAlchemyEmailWriteRepository


@dataclass
class SQLAlchemyEmailReadRepository(EmailReadRepositoryABC):
    db_session: AsyncSession

    async def load_by_conflict(self, external_id: str) -> Email | None:
        email = await self.db_session.scalar(
            select(SQLAlchemyEmail).where(SQLAlchemyEmail.external_id == external_id)
        )
        return Email.model_validate(email, from_attributes=True) if email else None

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

    # UGLY: сложно реализовать настоящий change tracking
    # возможно подойдет сделать Email протоколом для утиной типизации и использовать инстанс SQLAlchemyEmail,
    # но тогда проблемы с валидацией появляются, которые по идее легко решаются

    async def insert(self, email: Email) -> None:
        return self.db_session.add(SQLAlchemyEmail(**email.model_dump()))

    async def update_status(self, email: Email) -> None:
        await self.db_session.execute(
            update(SQLAlchemyEmail)
            .where(SQLAlchemyEmail.id == email.id)
            .values(status=email.status)
        )

    async def insert_domain_event(self, event: EmailBaseEvent) -> None:
        await self.db_session.execute(
            insert(SQLAlchemyEmailEvent).values(
                email_id=event.email_id,
                timestamp=event.timestamp,
                event=event.event,
                event_data=event.event_data,
            )
        )

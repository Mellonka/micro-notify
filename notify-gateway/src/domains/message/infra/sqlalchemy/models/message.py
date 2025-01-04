from uuid import UUID, uuid4
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.domains.message.infra.sqlalchemy.metadata import Base


class MessageDB(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    external_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    reciver: Mapped[str] = mapped_column(nullable=False)
    sender: Mapped[str] = mapped_column(nullable=False)
    pending: Mapped[bool] = mapped_column(nullable=False, default=False)
    text: Mapped[str] = mapped_column()
    meta: Mapped[dict] = mapped_column(JSON)

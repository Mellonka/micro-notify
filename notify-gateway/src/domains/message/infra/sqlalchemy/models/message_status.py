from datetime import datetime
from sqlalchemy import UUID, Column, String, DateTime

from src.domains.message.infra.sqlalchemy.metadata import Base

class MessageStatusDB(Base):
    __tablename__="message_statues"

    id = Column(UUID, primary_key=True)
    status = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.now())


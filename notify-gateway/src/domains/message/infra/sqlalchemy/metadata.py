from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from src.config import POSTGRES_URL

Base = declarative_base()

engine: AsyncEngine = create_async_engine(
    url=POSTGRES_URL,
)

session_factory: async_sessionmaker = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)

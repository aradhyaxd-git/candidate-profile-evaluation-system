import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase
)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment")
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": True}
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

import asyncio

from app.core.database import engine, Base
from app.models import db_models  # IMPORTANT: this imports the models


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())

import asyncio

from Database.database import engine
from Database.models import Base
import Database.models   # forces model registration


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully")

asyncio.run(main())

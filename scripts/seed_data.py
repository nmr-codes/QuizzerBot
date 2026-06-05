"""Seed initial settings and admin user for development."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal, engine


async def seed():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # Placeholder: insert default settings if needed
        print("Seeding default settings... (no-op placeholder)")


if __name__ == "__main__":
    asyncio.run(seed())

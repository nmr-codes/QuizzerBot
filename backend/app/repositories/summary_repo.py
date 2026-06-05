from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.summary import Summary


class SummaryRepository(BaseRepository[Summary]):
    def __init__(self, db: AsyncSession):
        super().__init__(Summary, db)

    async def get_by_upload(self, upload_id: UUID) -> Optional[Summary]:
        result = await self.db.execute(select(self.model).where(self.model.upload_id == upload_id))
        return result.scalar_one_or_none()

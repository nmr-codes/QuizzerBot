from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.repositories.base import BaseRepository
from app.models.upload import Upload


class UploadRepository(BaseRepository[Upload]):
    def __init__(self, db: AsyncSession):
        super().__init__(Upload, db)

    async def get_by_content_hash(self, content_hash: str) -> Optional[Upload]:
        result = await self.db.execute(
            "SELECT * FROM uploads WHERE content_hash = :ch",
            {"ch": content_hash},
        )
        row = result.first()
        if not row:
            return None
        # row is a SQLAlchemy Row; map to model via primary key
        return await self.get(row.id)

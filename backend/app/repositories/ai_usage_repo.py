from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.ai_usage_log import AIUsageLog


class AIUsageRepository(BaseRepository[AIUsageLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(AIUsageLog, db)

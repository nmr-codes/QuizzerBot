from __future__ import annotations

import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class UserAchievement(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "user_achievements"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    achievement_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    earned_at: Mapped[datetime := __import__("datetime").datetime] = mapped_column(__import__("sqlalchemy").DateTime(timezone=True))
    notified: Mapped[bool] = mapped_column(__import__("sqlalchemy").Boolean, default=False)

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Credits(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "credits"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)
    lifetime_earned: Mapped[int] = mapped_column(Integer, default=0)
    lifetime_spent: Mapped[int] = mapped_column(Integer, default=0)

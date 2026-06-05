from __future__ import annotations

import uuid

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Achievement(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "achievements"

    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str | None] = mapped_column(String(10), nullable=True)
    xp_reward: Mapped[int] = mapped_column(Integer, default=0)
    credit_reward: Mapped[int] = mapped_column(Integer, default=0)
    condition_type: Mapped[str] = mapped_column(String(50), nullable=False)
    condition_value: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean := __import__("sqlalchemy").Boolean, default=True)

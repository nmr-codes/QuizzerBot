from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Plan(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "plans"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_uzs: Mapped[str] = mapped_column(String(50), nullable=False, default="0")
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    credits: Mapped[int] = mapped_column(Integer, default=0)
    bonus_credits: Mapped[int] = mapped_column(Integer, default=0)
    features: Mapped[dict] = mapped_column(JSONB, default=list)
    max_uploads_per_day: Mapped[int] = mapped_column(Integer, default=-1)
    max_file_size_mb: Mapped[int] = mapped_column(Integer, default=10)
    priority_processing: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

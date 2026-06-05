from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Referral(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "referrals"

    referrer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    referred_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    referrer_reward: Mapped[int] = mapped_column(Integer, default=0)
    referred_reward: Mapped[int] = mapped_column(Integer, default=0)
    converted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rewarded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

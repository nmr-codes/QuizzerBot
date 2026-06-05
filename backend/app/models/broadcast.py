from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Broadcast(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "broadcasts"

    admin_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    text_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    buttons: Mapped[list] = mapped_column(JSONB, default=list)
    target_segment: Mapped[str] = mapped_column(String(30), default="all")
    segment_filter: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    scheduled_at: Mapped[datetime | None] = mapped_column(__import__("sqlalchemy").DateTime(timezone=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(__import__("sqlalchemy").DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(__import__("sqlalchemy").DateTime(timezone=True), nullable=True)
    total_recipients: Mapped[int] = mapped_column(Integer, default=0)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)

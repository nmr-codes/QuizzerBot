from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Summary(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "summaries"

    upload_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    key_concepts: Mapped[list] = mapped_column(JSONB, default=list)
    definitions: Mapped[list] = mapped_column(JSONB, default=list)
    word_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

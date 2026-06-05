from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class FlashcardSet(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "flashcard_sets"

    upload_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    card_count: Mapped[int] = mapped_column(Integer, nullable=False)
    cards: Mapped[list] = mapped_column(JSONB, nullable=False)

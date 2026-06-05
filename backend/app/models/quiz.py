from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class Quiz(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "quizzes"

    upload_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(10), default="medium")
    question_count: Mapped[int] = mapped_column(Integer, nullable=False)
    question_types: Mapped[list] = mapped_column(JSONB, default=list)
    questions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_adaptive: Mapped[bool] = mapped_column(Boolean, default=False)
    weak_topics: Mapped[list] = mapped_column(JSONB, default=list)
    total_attempts: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="quizzes")

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class QuizSession(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "quiz_sessions"

    quiz_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    mode: Mapped[str] = mapped_column(String(20), default="practice")
    status: Mapped[str] = mapped_column(String(20), default="in_progress")
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    answered_questions: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    wrong_answers: Mapped[int] = mapped_column(Integer, default=0)
    skipped_answers: Mapped[int] = mapped_column(Integer, default=0)
    score_percentage: Mapped[str | None] = mapped_column(DECIMAL(5, 2), nullable=True)
    time_limit_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_spent_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    detailed_results: Mapped[list] = mapped_column(JSONB, default=list)

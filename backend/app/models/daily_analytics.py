from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import Column, Integer, Date, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class DailyAnalytics(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "daily_analytics"

    date: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    new_users: Mapped[int] = mapped_column(Integer, default=0)
    active_users: Mapped[int] = mapped_column(Integer, default=0)
    total_uploads: Mapped[int] = mapped_column(Integer, default=0)
    total_quizzes: Mapped[int] = mapped_column(Integer, default=0)
    total_flashcards: Mapped[int] = mapped_column(Integer, default=0)
    total_summaries: Mapped[int] = mapped_column(Integer, default=0)
    quiz_sessions: Mapped[int] = mapped_column(Integer, default=0)
    revenue_uzs: Mapped[str] = mapped_column(String := __import__("sqlalchemy").String, default="0")
    new_subscriptions: Mapped[int] = mapped_column(Integer, default=0)
    ai_tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    ai_cost_usd: Mapped[str] = mapped_column(String, default="0")

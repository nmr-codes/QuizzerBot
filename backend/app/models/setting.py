from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Setting(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    type: Mapped[str] = mapped_column(String(20), default="string")
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_secret: Mapped[bool] = mapped_column(__import__("sqlalchemy").Boolean, default=False)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

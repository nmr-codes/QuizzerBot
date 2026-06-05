from __future__ import annotations

from pydantic import BaseModel


class UserCreate(BaseModel):
    telegram_id: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None


class UserRead(BaseModel):
    id: str
    telegram_id: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True

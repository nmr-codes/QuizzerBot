from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "QuizMaster AI"
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "change-me"
    allowed_hosts: List[str] = ["*"]
    allowed_origins: List[str] = ["*"]

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/quizmaster"
    database_pool_size: int = 20
    database_max_overflow: int = 40

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_db: int = 1
    redis_rate_limit_db: int = 2

    # Bot
    telegram_bot_token: str = ""
    webhook_url: str | None = None
    webhook_secret: str | None = None
    admin_telegram_ids: List[int] = []
    owner_telegram_id: int | None = None

    # AI
    gemini_api_keys: List[str] = []
    gemini_model: str = "gemini-1.5-flash"

    # Storage
    storage_backend: str = "local"
    storage_local_path: str = "/app/storage"
    storage_max_file_size_mb: int = 50

    # JWT
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 30

    # Celery
    celery_broker_url: str = "redis://localhost:6379/3"
    celery_result_backend: str = "redis://localhost:6379/4"

    # Admin
    admin_secret: str = "change-me-admin-secret"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

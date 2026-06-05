from functools import lru_cache
import os

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # App
    app_name: str = Field("QuizMaster AI", alias="APP_NAME")
    app_env: str = Field("development", alias="APP_ENV")
    debug: bool = Field(False, alias="DEBUG")
    secret_key: str = Field("change-me", alias="SECRET_KEY")
    allowed_hosts: list[str] = Field(default_factory=list, alias="ALLOWED_HOSTS")
    allowed_origins: list[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")

    # Database
    database_url: str = Field(
        "******localhost:5432/quizmaster",
        alias="DATABASE_URL",
    )
    database_pool_size: int = Field(20, alias="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(40, alias="DATABASE_MAX_OVERFLOW")

    # Redis
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")
    redis_cache_db: int = Field(1, alias="REDIS_CACHE_DB")
    redis_rate_limit_db: int = Field(2, alias="REDIS_RATE_LIMIT_DB")

    # Bot
    telegram_bot_token: str = Field("", alias="BOT_TOKEN")
    webhook_url: str | None = Field(None, alias="WEBHOOK_URL")
    webhook_secret: str | None = Field(None, alias="WEBHOOK_SECRET")
    admin_telegram_ids: list[int] = Field(default_factory=list, alias="ADMIN_TELEGRAM_IDS")
    owner_telegram_id: int | None = Field(None, alias="OWNER_TELEGRAM_ID")

    # AI
    gemini_api_keys: list[str] = Field(default_factory=list, alias="GEMINI_API_KEYS")
    gemini_model: str = Field("gemini-1.5-flash", alias="GEMINI_MODEL")

    # Storage
    storage_backend: str = Field("local", alias="STORAGE_BACKEND")
    storage_local_path: str = Field("/app/storage", alias="STORAGE_LOCAL_PATH")
    storage_max_file_size_mb: int = Field(50, alias="STORAGE_MAX_FILE_SIZE_MB")

    # JWT
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(60, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(30, alias="JWT_REFRESH_TOKEN_EXPIRE_DAYS")

    # Celery
    celery_broker_url: str = Field("redis://localhost:6379/3", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field("redis://localhost:6379/4", alias="CELERY_RESULT_BACKEND")

    # Admin
    admin_secret: str = Field("change-me-admin-secret", alias="ADMIN_SECRET_KEY")
    admin_session_expire_hours: int = Field(24, alias="ADMIN_SESSION_EXPIRE_HOURS")

    # Payments
    click_merchant_id: str | None = Field(None, alias="CLICK_MERCHANT_ID")
    click_secret_key: str | None = Field(None, alias="CLICK_SECRET_KEY")
    payme_merchant_id: str | None = Field(None, alias="PAYME_MERCHANT_ID")
    payme_secret_key: str | None = Field(None, alias="PAYME_SECRET_KEY")
    uzum_merchant_id: str | None = Field(None, alias="UZUM_MERCHANT_ID")
    uzum_secret_key: str | None = Field(None, alias="UZUM_SECRET_KEY")
    paynet_merchant_id: str | None = Field(None, alias="PAYNET_MERCHANT_ID")
    paynet_secret_key: str | None = Field(None, alias="PAYNET_SECRET_KEY")

    # Monitoring
    sentry_dsn: str | None = Field(None, alias="SENTRY_DSN")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    # Security
    rate_limit_default: str = Field("100/minute", alias="RATE_LIMIT_DEFAULT")
    auto_create_tables: bool = Field(False, alias="AUTO_CREATE_TABLES")

    @field_validator("allowed_hosts", "allowed_origins", mode="before")
    @classmethod
    def _split_csv(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("admin_telegram_ids", mode="before")
    @classmethod
    def _split_admin_ids(cls, value):
        if value is None or value == "":
            return []
        if isinstance(value, str):
            return [int(item.strip()) for item in value.split(",") if item.strip().isdigit()]
        return value

    @field_validator("gemini_api_keys", mode="before")
    @classmethod
    def _split_gemini_keys(cls, value):
        if value is None or value == "":
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @model_validator(mode="after")
    def _normalize_settings(self):
        if not self.allowed_hosts:
            self.allowed_hosts = ["*"]
        if not self.allowed_origins:
            self.allowed_origins = ["*"]
        if not self.gemini_api_keys:
            keys: list[str] = []
            for idx in range(1, 10):
                key = os.getenv(f"GEMINI_API_KEY_{idx}")
                if key:
                    keys.append(key)
            if keys:
                self.gemini_api_keys = keys
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

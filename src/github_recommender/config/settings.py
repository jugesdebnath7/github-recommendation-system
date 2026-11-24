
# src/github_recommender/config/settings.py

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    url: PostgresDsn = Field(
        ...,
        description="PostgreSQL database URL",
    )

    pool_size: int = Field(default=5, ge=1)
    pool_timeout: float = Field(default=30, gt=0)
    max_overflow: int = Field(default=10, ge=0)
    pool_recycle: int = Field(default=1800, gt=0)

    @property
    def dsn(self) -> str:
        return str(self.url)


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    # Application
    env: Literal["development", "staging", "production"] = "development"

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    # Database
    database: DatabaseSettings = Field(...)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

import secrets
from typing import Literal

from pydantic import (
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=(".env", "../.env"), env_file_encoding="utf-8"
    )
    # for debug
    VERSION: str
    SECRET: str = secrets.token_urlsafe(32)
    # 60 * 24 * 7 = 168 = 7 days
    TTL_TOKEN: int = 60 * 24 * 7
    ENVIRONMENT: Literal["local", "staging", "production"]
    FE_HOST_PORT: int
    BE_HOST_PORT: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def FRONTEND(self) -> str:
        return f"http://{self.APP_HOST}:{self.FE_HOST_PORT}"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def BACKEND(self) -> list[str]:
        return [f"http://{self.APP_HOST}:{self.BE_HOST_PORT}"]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND] + [self.FRONTEND]

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    APP_HOST: str
    DB_HOST_PORT: int
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.APP_HOST,
            port=self.DB_HOST_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore

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
        # Use top level .env file (one level above ./be/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    VERSION: str
    SECRET: str = secrets.token_urlsafe(32)
    # 60 * 24 * 7 = 168 = 7 days
    TTL_TOKEN: int = 60 * 24 * 7
    ENVIRONMENT: Literal["local", "staging", "production"]
    APP_HOST: str
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
    APP_HOST: str  # this is because docker service name is used as host
    DB_HOST_PORT: int  # this is because docker service name is used as host
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
            host=self.APP_HOST,  # this is because docker service name is used as host
            port=self.DB_HOST_PORT,  # this is because docker service name is used as host
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore

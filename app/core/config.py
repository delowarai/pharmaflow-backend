from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="PharmaFlow", validation_alias="APP_NAME")
    app_version: str = Field(default="1.0.0", validation_alias="APP_VERSION")
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    database_url: str = Field(
        default="sqlite:///./pharmaflow.db",
        validation_alias="DATABASE_URL",
    )
    jwt_secret: str = Field(
        default="development-secret-change-before-production",
        validation_alias="JWT_SECRET",
    )
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    refresh_token_expire_days: int = Field(
        default=7,
        validation_alias="REFRESH_TOKEN_EXPIRE_DAYS",
    )
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        validation_alias="CORS_ORIGINS",
    )
    ai_api_key: str = Field(default="", validation_alias="AI_API_KEY")
    ai_model: str = Field(default="gpt-4o-mini", validation_alias="AI_MODEL")
    ai_base_url: str = Field(
        default="https://api.openai.com/v1",
        validation_alias="AI_BASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP__",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    db: DatabaseConfig


settings = Settings()

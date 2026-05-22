from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str = Field(alias="BOT_TOKEN")
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    database_url: str = Field(alias="DATABASE_URL")
    reminder_hour_utc: int = Field(default=9, alias="REMINDER_HOUR_UTC")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

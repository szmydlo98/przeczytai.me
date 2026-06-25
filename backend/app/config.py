from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

    max_text_chars: int = 100_000
    readings_table_name: str = Field(
        default="local-readings",
        validation_alias=AliasChoices(
            "READINGS_TABLE_NAME",
            "TEXTS_TABLE_NAME",
        ),
    )
    processor_function_name: str | None = Field(
        default=None,
        validation_alias="PROCESSOR_FUNCTION_NAME",
    )
    files_bucket_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("FILES_BUCKET_NAME", "TEXTS_BUCKET_NAME"),
    )
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    openai_api_key_secret_arn: str | None = Field(
        default=None,
        validation_alias=AliasChoices("OPENAI_API_KEY_SECRET_ARN", "OPENAI_API_KEY_SECRET_ID"),
    )
    openai_tts_enabled: bool | None = Field(default=None, validation_alias="OPENAI_TTS_ENABLED")


@lru_cache
def get_settings() -> Settings:
    return Settings()

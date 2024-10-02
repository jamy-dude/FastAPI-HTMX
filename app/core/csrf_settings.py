from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal

class CsrfSettings(BaseSettings):
    secret_key: str = Field(..., validation_alias="CSRF_SECRET_KEY")
    cookie_samesite: Literal["strict", "lax", "none"] = Field("lax", validation_alias="COOKIE_SAMESITE")
    cookie_secure: bool = Field(False, validation_alias="COOKIE_SECURE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

csrf_settings = CsrfSettings()
print(csrf_settings.secret_key)
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EduGenie"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    demo_mode: bool = False
    cors_origins: str = "*"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()] or ["*"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

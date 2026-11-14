from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    runpod_api_key: str
    runpod_endpoint_id: str = "ejj95trq8vd2iu"
    runpod_api_base: str = "https://api.runpod.ai/v2"
    runpod_timeout_seconds: float = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OUTPUT_FOLDER: str = "output"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

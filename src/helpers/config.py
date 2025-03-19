from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):

    APP_NAME: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int

    MONGO_URL: str
    MONGO_DB: str

    class Config:
        env_file = ".env"

def get_settings():
    return settings()
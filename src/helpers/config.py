from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):

    APP_NAME: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int

    MONGO_URL: str
    MONGO_DB: str

    GENERATION_MODEL: str
    EMBEDDING_MODEL: str

    OPENAI_API_KEY: str = None
    OPENAI_URL: str = None
    COHERE_API_KEY: str = None

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    INPUT_MAX_CHARACTERS: int = None
    OUTPUT_MAX_TOKENS: int = None
    TEMPERATURE: float = None

    class Config:
        env_file = ".env"

def get_settings():
    return settings()
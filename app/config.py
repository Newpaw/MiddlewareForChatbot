from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MiddlewareForChatbot"
    PROJECT_VERSION: str = "1.0.1"
    LOG_LEVEL: str = "DEBUG"
    BASE_URL_ASSISTENT: str
    CHATBOT_ID: str
    BASE_URL_MLUVII: str
    CLIENT_ID:str
    CLIENT_SECRET:str
    REDIS_HOST:str
    REDIS_PORT:int
    REDIS_DB:int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

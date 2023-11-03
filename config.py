from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    CHAT_ID: int
    BOT_TOKEN: str

    API_LOG_LEVEL: str
    TELEGRAM_LOG_LEVEL: str

    class Config:
        env_file = ".env"


settings = Settings()

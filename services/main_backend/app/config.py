import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT: int = os.getenv("RABBITMQ_PORT", 5672)
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "")

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()

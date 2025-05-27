from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # RabbitMQ settings
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE: str

    # Email settings
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str

    # API settings
    API_HOST: str
    API_PORT: int
    DEBUG: bool = False

    class Config:
        env_file = ".envs/.local/.notifications"

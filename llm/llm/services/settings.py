from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API settings
    API_HOST: str
    API_PORT: int
    DEBUG: bool = False

    # OpenRouter settings
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    MODEL: str

    class Config:
        env_file = ".envs/.local/.llm" 
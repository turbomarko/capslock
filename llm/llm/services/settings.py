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

    # Rate limiting settings
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60  # Default to 60 requests per minute
    RATE_LIMIT_BURST_SIZE: int = 10  # Allow bursts of up to 10 requests

    class Config:
        env_file = ".envs/.local/.llm" 
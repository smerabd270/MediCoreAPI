from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MediCore API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_SERVER: str
    DATABASE_PORT: int = 1433
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_TRUST_SERVER_CERTIFICATE: bool = True

    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int = 60

    AI_PROVIDER: str = "ollama"
    OPENAI_API_KEY: str = "your-openai-api-key"
    MODEL_NAME: str = "gpt-4o"
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_NAME: str = "llama3.2"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

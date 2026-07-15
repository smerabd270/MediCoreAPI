from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "MediCore API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True


    # SQL Server
    DATABASE_SERVER: str
    DATABASE_PORT: int = 1433
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_TRUST_SERVER_CERTIFICATE: bool = True


    # Security
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int = 60


    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
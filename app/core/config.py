from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FavoredCoffee API"
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 día

    class Config:
        env_file = ".env"


settings = Settings()

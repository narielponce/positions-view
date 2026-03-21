from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/position_view"
    APP_NAME: str = "Position View API"

    class Config:
        env_file = ".env"


settings = Settings()

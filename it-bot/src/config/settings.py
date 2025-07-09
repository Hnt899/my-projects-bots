from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # TODO Make .env file and write there the same variables
    PROJECT_NAME: str = "basebot_template"

    DB_USERNAME: str = "base_bot"
    DB_PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_DATABASE: str = "base_database"
    DB_SCHEMA: str = ""

    BOT_TOKEN: str = ""
    BOT_NAME: str = ""

    LOG_LEVEL: str = "DEBUG"
    # TODO There is a LOG_STREAM for development. Switch it to False when prodaction
    LOG_STREAM: bool = True
    LOG_FILE: bool = True


settings = Settings()

DSN = (
    f"postgresql+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
)

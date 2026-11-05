from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    COMPLAINT_UPLOAD_DIR: str
    REPAIR_UPLOAD_DIR: str
    MAX_FILE_SIZE: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    TEST_DATABASE_URL: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env")


settings: Settings = Settings()

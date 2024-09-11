

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    SMTP_PROVIDER: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str

    SECRET_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()


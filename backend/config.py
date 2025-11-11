from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    
    API_URL: str
    FRONTEND_URL: str
    DATABASE_URL: str
    TOKEN_SECRET: str
    TOKEN_HOURS_DURATION: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    class Config:
        # Asegura que Pydantic lea el archivo .env que está junto a este archivo (backend/.env)
        env_file = str(Path(__file__).resolve().parent / '.env')
        env_file_encoding = 'utf-8'


settings = Settings()
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    API_URL: str
    FRONTEND_URL: str
    DATABASE_URL: str
    TOKEN_SECRET: str
    TOKEN_HOURS_DURATION: int

    # Configuración de envío de mails.
    # Optional para que el backend no se caiga si en algún entorno faltan estas variables.
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None

    class Config:
        # Asegura que Pydantic lea el archivo .env que está junto a este archivo (backend/.env)
        env_file = str(Path(__file__).resolve().parent / '.env')
        env_file_encoding = 'utf-8'


settings = Settings()
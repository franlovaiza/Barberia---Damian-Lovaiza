from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    API_URL: str
    FRONTEND_URL: str
    DATABASE_URL: str
    TOKEN_SECRET: str
    TOKEN_HOURS_DURATION: int

    # Configuración de envío de mails con Resend.
    # Optional para que el backend no se caiga si en algún entorno faltan estas variables
    # (por ejemplo, en tu compu si todavía no las cargaste en el .env).
    RESEND_API_KEY: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    
    class Config:
        # Asegura que Pydantic lea el archivo .env que está junto a este archivo (backend/.env)
        env_file = str(Path(__file__).resolve().parent / '.env')
        env_file_encoding = 'utf-8'


settings = Settings()
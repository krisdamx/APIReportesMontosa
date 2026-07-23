"""
Configuración global de la aplicación.

Este módulo carga todas las variables de entorno utilizando
Pydantic Settings, proporcionando validación y autocompletado.

Uso:

from app.core.config import settings

print(settings.DB_HOST)
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Aplicación
    # ------------------------------------------------------------------
    APP_NAME: str = "Sales Analytics API"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"

    # ------------------------------------------------------------------
    # Base de Datos
    # ------------------------------------------------------------------
    DB_HOST: str
    DB_PORT: int = 3306
    DB_DATABASE: str
    DB_USER: str
    DB_PASSWORD: str

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------
    STORAGE_PATH: Path = BASE_DIR / "storage"
    CSV_PATH: Path = BASE_DIR / "storage" / "csv"
    EXCEL_PATH: Path = BASE_DIR / "storage" / "excel"

    # ------------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------------
    MAX_UPLOAD_SIZE: int = 300 * 1024 * 1024  # 300 MB

    # ------------------------------------------------------------------
    # SQLAlchemy
    # ------------------------------------------------------------------
    SQL_ECHO: bool = False

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://"
            f"{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_DATABASE}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

# Crear automáticamente las carpetas necesarias
settings.STORAGE_PATH.mkdir(parents=True, exist_ok=True)
settings.CSV_PATH.mkdir(parents=True, exist_ok=True)
settings.EXCEL_PATH.mkdir(parents=True, exist_ok=True)
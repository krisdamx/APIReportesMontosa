"""
Global Logger Configuration.

Se utiliza en toda la aplicación.

Uso:

from app.core.logger import logger

logger.info("Servidor iniciado")
logger.warning("Archivo duplicado")
logger.error("Error al importar CSV")
"""

from pathlib import Path
import sys

from loguru import logger

from app.core.config import settings


# ==========================================================
# Directorio de logs
# ==========================================================

LOG_PATH = settings.STORAGE_PATH.parent / "logs"
LOG_PATH.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Eliminar configuración por defecto
# ==========================================================

logger.remove()


# ==========================================================
# Consola
# ==========================================================

logger.add(
    sys.stdout,
    level="DEBUG" if settings.APP_ENV == "development" else "INFO",
    colorize=True,
    enqueue=True,
    backtrace=True,
    diagnose=settings.APP_ENV == "development",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)


# ==========================================================
# Archivo
# ==========================================================

logger.add(
    LOG_PATH / "application.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    encoding="utf-8",
    level="INFO",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)


__all__ = ("logger",)
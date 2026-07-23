"""
Database configuration.

Este módulo centraliza toda la configuración relacionada con SQLAlchemy.

Expone:

- engine
- SessionLocal
- get_db()
- Base

Todos los modelos deberán heredar de Base.
Todos los repositories utilizarán get_db().
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.base import Base
from app.core.config import settings


# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,

    # Verifica que la conexión siga viva antes de utilizarla.
    pool_pre_ping=True,

    # Evita conexiones expiradas por timeout de MySQL.
    pool_recycle=3600,

    # Pool inicial.
    pool_size=10,

    # Conexiones extra si el pool se llena.
    max_overflow=20,
)


# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# ==========================================================
# Dependency Injection
# ==========================================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency para FastAPI.

    Ejemplo:

        @router.get("/")
        def get_data(db: Session = Depends(get_db)):
            ...
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# Exportaciones públicas
# ==========================================================

__all__ = (
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
)
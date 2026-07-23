"""
Base declarativa para todos los modelos de SQLAlchemy.

Todos los modelos deben heredar de Base.

Ejemplo:

class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
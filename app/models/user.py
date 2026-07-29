from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_entity import BaseEntity


class User(BaseEntity):
    __tablename__ = "usuarios"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
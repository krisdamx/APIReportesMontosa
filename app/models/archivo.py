from sqlalchemy import BigInteger, Enum, String, Text

from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import ImportStatus
from app.models.base_entity import BaseEntity


class Archivo(BaseEntity):

    __tablename__ = "archivos"

    nombre_original: Mapped[str] = mapped_column(String(255))

    nombre_storage: Mapped[str] = mapped_column(String(255))

    storage_path: Mapped[str] = mapped_column(String(500))

    file_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    extension: Mapped[str] = mapped_column(String(10))

    mime_type: Mapped[str] = mapped_column(String(120))

    file_size: Mapped[int] = mapped_column(BigInteger)

    total_registros: Mapped[int] = mapped_column(default=0)

    processing_time_ms: Mapped[int | None] = mapped_column(nullable=True)

    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus),
        default=ImportStatus.PENDING,
    )

    error_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
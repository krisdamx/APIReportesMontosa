from datetime import date

from sqlalchemy import DECIMAL, ForeignKey, SmallInteger, String

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_entity import BaseEntity


class Venta(BaseEntity):

    __tablename__ = "ventas"

    archivo_id: Mapped[int] = mapped_column(
        ForeignKey("archivos.id"),
        index=True,
    )

    business_key: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    frog_id: Mapped[str] = mapped_column(
        String(150),
        index=True,
    )

    factura: Mapped[str | None] = mapped_column(String(100))

    cliente: Mapped[str | None] = mapped_column(String(255))

    fecha_liquidacion: Mapped[date | None]

    fabricante: Mapped[str | None] = mapped_column(String(150))

    preventa: Mapped[str | None] = mapped_column(String(150))

    reparto: Mapped[str | None] = mapped_column(String(150))

    denominacion_comercial: Mapped[str | None] = mapped_column(String(255))

    producto: Mapped[str | None] = mapped_column(String(255))

    descripcion_canal: Mapped[str | None] = mapped_column(String(150))

    marca: Mapped[str | None] = mapped_column(String(150))

    presentacion: Mapped[str | None] = mapped_column(String(150))

    cajas: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    unidad: Mapped[str | None] = mapped_column(String(50))

    multiplo: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    importe_bruto: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    total: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    factor_conversion_1: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    factor_conversion_3: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    hlt: Mapped[float | None] = mapped_column(DECIMAL(18, 4))

    descripcion_producto: Mapped[str | None] = mapped_column(String(255))

    plaza: Mapped[str | None] = mapped_column(String(100))

    canal: Mapped[str | None] = mapped_column(String(100))

    clasificacion: Mapped[str | None] = mapped_column(String(100))

    cf: Mapped[str | None] = mapped_column(String(50))

    sabor: Mapped[str | None] = mapped_column(String(100))

    compania: Mapped[str | None] = mapped_column(String(150))

    anio: Mapped[int | None] = mapped_column(SmallInteger)
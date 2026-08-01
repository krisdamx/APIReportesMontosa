import polars as pl

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.venta import Venta


class DashboardRepository:

    @staticmethod
    def get_sales_dataframe(
        db: Session,
    ) -> pl.DataFrame:

        stmt = select(
            Venta.fabricante,
            Venta.marca,
            Venta.plaza,
            Venta.canal,
            Venta.compania,
            Venta.producto,
            Venta.descripcion_producto,
            Venta.presentacion,
            Venta.sabor,
            Venta.clasificacion,
            Venta.anio,
        )

        result = db.execute(stmt)

        rows = [
            dict(row._mapping)
            for row in result
        ]

        return pl.DataFrame(rows)
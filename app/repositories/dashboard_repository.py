import polars as pl

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.venta import Venta

COLUMN_MAP = {
    "fabricante": Venta.fabricante,
    "marca": Venta.marca,
    "plaza": Venta.plaza,
    "canal": Venta.canal,
    "compania": Venta.compania,
    "producto": Venta.producto,
    "descripcion_producto": Venta.descripcion_producto,
    "presentacion": Venta.presentacion,
    "sabor": Venta.sabor,
    "clasificacion": Venta.clasificacion,
    "anio": Venta.anio,
    "total": Venta.total,
    "importe_bruto": Venta.importe_bruto,
    "cliente": Venta.cliente,
    "cf": Venta.cf,
    "hlt": Venta.hlt,
    "cajas": Venta.cajas,
    "frog_id": Venta.frog_id,
    "fecha_liquidacion": Venta.fecha_liquidacion,
}

class DashboardRepository:

    @staticmethod
    def get_sales_dataframe(
        db: Session,
        columns: list[str],
        fecha_inicio=None,
        fecha_fin=None,
        fabricante=None,
        marca=None,
        plaza=None,
        canal=None,
        compania=None,
        producto=None,
        presentacion=None,
        sabor=None,
        clasificacion=None,
        anio=None,
    ) -> pl.DataFrame:

        stmt = select(
            *[
                COLUMN_MAP[column]
                for column in columns
            ]
        )

        if fecha_inicio:
            stmt = stmt.where(
                Venta.fecha_liquidacion >= fecha_inicio
            )

        if fecha_fin:
            stmt = stmt.where(
                Venta.fecha_liquidacion <= fecha_fin
            )

        if fabricante:
            stmt = stmt.where(
                Venta.fabricante == fabricante
            )

        if marca:
            stmt = stmt.where(
                Venta.marca == marca
            )

        if plaza:
            stmt = stmt.where(
                Venta.plaza == plaza
            )

        if canal:
            stmt = stmt.where(
                Venta.canal == canal
            )

        if compania:
            stmt = stmt.where(
                Venta.compania == compania
            )

        if producto:
            stmt = stmt.where(
                Venta.producto == producto
            )

        if presentacion:
            stmt = stmt.where(
                Venta.presentacion == presentacion
            )

        if sabor:
            stmt = stmt.where(
                Venta.sabor == sabor
            )

        if clasificacion:
            stmt = stmt.where(
                Venta.clasificacion == clasificacion
            )

        if anio:
            stmt = stmt.where(
                Venta.anio == anio
            )

        result = db.execute(stmt)

        rows = [
            dict(row._mapping)
            for row in result
        ]

        return pl.DataFrame(rows)
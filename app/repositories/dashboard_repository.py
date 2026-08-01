import polars as pl

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.venta import Venta


class DashboardRepository:

    @staticmethod
    def get_sales_dataframe(
        db: Session,
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

            # Datos para Summary
            Venta.total,
            Venta.cliente,
            Venta.cf,
            Venta.hlt,
            Venta.cajas,
            Venta.frog_id,
            Venta.fecha_liquidacion,
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
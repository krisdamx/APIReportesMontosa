import polars as pl
from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    @staticmethod
    def _catalog(
        df: pl.DataFrame,
        column: str,
    ):

        values = (
            df
            .select(column)
            .drop_nulls()
            .unique()
            .sort(column)
            .to_series()
            .to_list()
        )

        values = sorted({
            str(value).strip()
            for value in values
            if str(value).strip() not in ("", "#N/D")
        })

        return [
            {
                "label": str(value).strip(),
                "value": str(value).strip(),
            }
            for value in values
        ]

    @staticmethod
    def _product_catalog(df: pl.DataFrame):

        productos = (
            df
            .select(
                [
                    "producto",
                    "descripcion_producto",
                ]
            )
            .drop_nulls()
            .unique()
            .sort("descripcion_producto")
            .to_dicts()
        )

        return [
            {
                "label": item["descripcion_producto"],
                "value": str(item["producto"]),
            }
            for item in productos
        ]

    @classmethod
    def get_catalogs(
        cls,
        db: Session,
    ):

        df = DashboardRepository.get_sales_dataframe(db)

        return {
            "fabricantes": cls._catalog(df, "fabricante"),
            "marcas": cls._catalog(df, "marca"),
            "plazas": cls._catalog(df, "plaza"),
            "canales": cls._catalog(df, "canal"),
            "companias": cls._catalog(df, "compania"),
            "productos": cls._product_catalog(df),
            "presentaciones": cls._catalog(df, "presentacion"),
            "sabores": cls._catalog(df, "sabor"),
            "clasificaciones": cls._catalog(df, "clasificacion"),
            "anios": cls._catalog(df, "anio"),
        }

    @classmethod
    def get_summary(
        cls,
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
    ):

        df = DashboardRepository.get_sales_dataframe(
            db=db,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fabricante=fabricante,
            marca=marca,
            plaza=plaza,
            canal=canal,
            compania=compania,
            producto=producto,
            presentacion=presentacion,
            sabor=sabor,
            clasificacion=clasificacion,
            anio=anio,
        )

        if df.is_empty():
            return {
                "ventas": 0,
                "clientes": 0,
                "cf": 0,
                "hlt": 0,
                "cajas": 0,
                "pedidos": 0,
                "ticketPromedio": 0,
            }

        ventas = float(df["total"].fill_null(0).sum())

        clientes = df["cliente"].n_unique()

        cf = float(df["cf"].fill_null(0).sum())

        hlt = float(df["hlt"].fill_null(0).sum())

        cajas = float(df["cajas"].fill_null(0).sum())

        pedidos = df["frog_id"].n_unique()

        ticket_promedio = (
            ventas / pedidos
            if pedidos > 0
            else 0
        )

        return {
            "ventas": round(ventas, 2),
            "clientes": clientes,
            "cf": round(cf, 2),
            "hlt": round(hlt, 2),
            "cajas": round(cajas, 2),
            "pedidos": pedidos,
            "ticketPromedio": round(ticket_promedio, 2),
        }
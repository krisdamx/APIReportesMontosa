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

        return [
            {
                "label": str(value),
                "value": str(value),
            }
            for value in values
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
            "anios": cls._catalog(df, "anio"),
        }

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
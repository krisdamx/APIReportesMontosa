from decimal import Decimal

import polars as pl
from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.services.dashboard_analytics_engine import DashboardAnalyticsEngine


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
    def _product_catalog(
        df: pl.DataFrame,
    ):

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

    @staticmethod
    def _normalize_data(
        rows: list[dict],
    ) -> list[dict]:

        normalized = []

        for row in rows:

            item = {}

            for key, value in row.items():

                if isinstance(value, Decimal):
                    item[key] = round(float(value), 2)

                elif isinstance(value, float):
                    item[key] = round(value, 2)

                else:
                    item[key] = value

            normalized.append(item)

        return normalized


    @staticmethod
    def _summary_from_dataframe(
        df: pl.DataFrame,
    ) -> dict:

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

        ventas = float(
            df["total"]
            .fill_null(0)
            .sum()
        )

        clientes = (
            df["cliente"]
            .n_unique()
            if "cliente" in df.columns
            else 0
        )

        cf = (
            float(
                df["cf"]
                .cast(pl.Float64, strict=False)
                .fill_null(0)
                .sum()
            )
            if "cf" in df.columns
            else 0
        )

        hlt = (
            float(
                df["hlt"]
                .fill_null(0)
                .sum()
            )
            if "hlt" in df.columns
            else 0
        )

        cajas = (
            float(
                df["cajas"]
                .fill_null(0)
                .sum()
            )
            if "cajas" in df.columns
            else 0
        )

        pedidos = (
            df["frog_id"].n_unique()
            if "frog_id" in df.columns
            else 0
        )

        ticket = (
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
            "ticketPromedio": round(ticket, 2),
        }

    @classmethod
    def get_catalogs(
        cls,
        db: Session,
    ):

        df = DashboardRepository.get_sales_dataframe(
            db=db,
            columns=[
                "fabricante",
                "marca",
                "plaza",
                "canal",
                "compania",
                "producto",
                "descripcion_producto",
                "presentacion",
                "sabor",
                "clasificacion",
                "anio",
            ],
        )

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
            columns=[
                "total",
                "cliente",
                "cf",
                "hlt",
                "cajas",
                "frog_id",
            ],
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

        cf = float(df["cf"].cast(pl.Float64, strict=False).fill_null(0).sum())

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

    @classmethod
    def get_analytics(
        cls,
        db: Session,
        metrics: list[str],
        group_by: list[str],
        order_by: str | None = None,
        order: str = "desc",
        limit: int | None = None,
        include_totals: bool = True,
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

        columns = DashboardAnalyticsEngine.required_columns(
            metrics=metrics,
            group_by=group_by,
        )

        df = DashboardRepository.get_sales_dataframe(
            db=db,
            columns=columns,
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

            totals = {}

            if include_totals:
                totals = {
                    metric: 0
                    for metric in metrics
                }

            return {
                "metadata": {
                    "metrics": metrics,
                    "groupBy": group_by,
                    "records": 0,
                },
                "totals": totals,
                "data": [],
            }

        result = DashboardAnalyticsEngine.build(
            df=df,
            metrics=metrics,
            group_by=group_by,
            order_by=order_by,
            order=order,
            limit=limit,
        )

        totals = {}

        if include_totals:

            summary = cls._summary_from_dataframe(df)

            totals = {
                metric: summary.get(metric, 0)
                for metric in metrics
            }

        return {
            "metadata": {
                "metrics": metrics,
                "groupBy": group_by,
                "records": result.height,
            },
            "totals": totals,
            "data": cls._normalize_data(
                result.to_dicts()
            ),
        }
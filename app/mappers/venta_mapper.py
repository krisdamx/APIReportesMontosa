import hashlib
from datetime import date, datetime

import polars as pl

from app.core.csv_columns import (
    FROG_ID,
    FACTURA,
    CLIENTE,
    FECHA_LIQUIDACION,
    FABRICANTE,
    PREVENTA,
    REPARTO,
    DENOMINACION_COMERCIAL,
    PRODUCTO,
    DESCRIPCION_CANAL,
    MARCA,
    PRESENTACION,
    CAJAS,
    UNIDAD,
    MULTIPLO,
    IMPORTE_BRUTO,
    TOTAL,
    FACTOR_CONVERSION_1,
    FACTOR_CONVERSION_3,
    HLT,
    DESCRIPCION_PRODUCTO,
    PLAZA,
    CANAL,
    CLASIFICACION,
    CF,
    SABOR,
    COMPANIA,
    ANIO,
)


class VentaMapper:

    @staticmethod
    def generate_business_key(
        frog_id: str,
        producto: str,
        presentacion: str,
    ) -> str:

        value = f"{frog_id}|{producto}|{presentacion}"

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

    @staticmethod

    @staticmethod
    def to_date(value):

        if value is None:
            return None

        if isinstance(value, date):
            return value

        if isinstance(value, datetime):
            return value.date()

        if value == "":
            return None

        return datetime.strptime(
            str(value),
            "%d/%m/%Y"
        ).date()

    @staticmethod
    def to_float(value) -> float | None:
        if value is None:
            return None

        text = str(value).strip()

        if text in ("", "-", "NULL", "None"):
            return None

        text = (
            text.replace("$", "")
                .replace(",", "")
                .strip()
        )

        return float(text)

    @classmethod
    def to_rows(
        cls,
        archivo_id: int,
        df: pl.DataFrame,
    ) -> list[dict]:

        rows = []

        for row in df.to_dicts():

            business_key = cls.generate_business_key(
                row[FROG_ID],
                row[PRODUCTO],
                row[PRESENTACION],
            )

            rows.append(
                {
                    "archivo_id": archivo_id,
                    "business_key": business_key,
                    "frog_id": row[FROG_ID],
                    "factura": row[FACTURA],
                    "cliente": row[CLIENTE],
                    "fecha_liquidacion": cls.to_date(row[FECHA_LIQUIDACION]),
                    "fabricante": row[FABRICANTE],
                    "preventa": row[PREVENTA],
                    "reparto": row[REPARTO],
                    "denominacion_comercial": row[DENOMINACION_COMERCIAL],
                    "producto": row[PRODUCTO],
                    "descripcion_canal": row[DESCRIPCION_CANAL],
                    "marca": row[MARCA],
                    "presentacion": row[PRESENTACION],
                    "unidad": row[UNIDAD],
                    "cajas": cls.to_float(row[CAJAS]),
                    "multiplo": cls.to_float(row[MULTIPLO]),
                    "importe_bruto": cls.to_float(row[IMPORTE_BRUTO]),
                    "total": cls.to_float(row[TOTAL]),
                    "factor_conversion_1": cls.to_float(row[FACTOR_CONVERSION_1]),
                    "factor_conversion_3": cls.to_float(row[FACTOR_CONVERSION_3]),
                    "hlt": cls.to_float(row[HLT]),
                    "descripcion_producto": row[DESCRIPCION_PRODUCTO],
                    "plaza": row[PLAZA],
                    "canal": row[CANAL],
                    "clasificacion": row[CLASIFICACION],
                    "cf": row[CF],
                    "sabor": row[SABOR],
                    "compania": row[COMPANIA],
                    "anio": int(row[ANIO]) if row[ANIO] not in (None, "") else None,
                }
            )

        return rows
"""
Application Constants.

Centraliza todas las constantes del proyecto para evitar
strings mágicos y valores repetidos.
"""

from enum import Enum


# ==========================================================
# Files
# ==========================================================

CSV_EXTENSION = ".csv"

EXCEL_EXTENSION = ".xlsx"

ALLOWED_EXTENSIONS = {
    CSV_EXTENSION,
}


# ==========================================================
# Upload
# ==========================================================

DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 MB

BATCH_SIZE = 1000


# ==========================================================
# Pagination
# ==========================================================

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 50

MAX_PAGE_SIZE = 500


# ==========================================================
# Date Formats
# ==========================================================

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ==========================================================
# Import Status
# ==========================================================

class ImportStatus(str, Enum):

    PENDING = "PENDING"

    PROCESSING = "PROCESSING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


# ==========================================================
# Report Types
# ==========================================================

class ReportType(str, Enum):

    REPORT_1 = "report_1"

    REPORT_2 = "report_2"

    REPORT_3 = "report_3"

    REPORT_4 = "report_4"


# ==========================================================
# CSV Column Mapping
# ==========================================================
#
# Clave:
#     Nombre EXACTO que viene en el CSV.
#
# Valor:
#     Nombre que utilizaremos internamente
#     tanto en Polars como en SQLAlchemy.
#
# Nunca utilizar directamente el nombre original
# del CSV dentro de la aplicación.
# ==========================================================

CSV_COLUMNS = {

    "FACTURA":
        "factura",

    "Cliente\n[Cliente]":
        "cliente",

    "Fecha de liquidación\n[Liquidación]":
        "fecha_liquidacion",

    "Descripción\nFabricante":
        "fabricante",

    "PREVENTA":
        "preventa",

    "REPARTO":
        "reparto",

    "Denominación comercial\n[Cliente]":
        "denominacion_comercial",

    "Producto\n[Pedido det.]":
        "producto",

    "Descripción\nCanal":
        "descripcion_canal",

    "Descripción\nMarca":
        "marca",

    "Descripción\nCatalogo presentaciones":
        "presentacion",

    "CAJAS":
        "cajas",

    "Unidad\n[Pedido det.]":
        "unidad",

    "Multiplica\n[Múltiplo producto]":
        "multiplo",

    " IMPORTE BRUTO S/IMP ":
        "importe_bruto",

    " TOTAL S/IMP ":
        "total",

    "Factor conversión 1\n[Producto]":
        "factor_conversion_1",

    "Factor conversión 3\n[Producto]":
        "factor_conversion_3",

    "HLT":
        "hlt",

    "Descripción\n[Producto]":
        "descripcion_producto",

    "PLAZA":
        "plaza",

    "CANAL":
        "canal",

    "CLASIF":
        "clasificacion",

    "CF":
        "cf",

    "SABOR":
        "sabor",

    "Compañía":
        "compania",

    "AÑO":
        "anio",
}


# ==========================================================
# Numeric Columns
# ==========================================================
#
# Estas columnas deberán convertirse
# automáticamente a valores numéricos.
# ==========================================================

NUMERIC_COLUMNS = {

    "cajas",

    "multiplo",

    "importe_bruto",

    "total",

    "factor_conversion_1",

    "factor_conversion_3",

    "hlt",

}


# ==========================================================
# Date Columns
# ==========================================================

DATE_COLUMNS = {

    "fecha_liquidacion",

}


# ==========================================================
# Dashboard Default Filters
# ==========================================================

DEFAULT_FILTERS = {

    "cliente",

    "plaza",

    "marca",

    "canal",

    "producto",

    "fabricante",

    "anio",

}
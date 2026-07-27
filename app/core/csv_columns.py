"""
Definición de columnas del CSV.

Este archivo es la única fuente de verdad para los nombres
de las columnas utilizadas durante la importación.
"""

# ==========================
# Nombres internos
# ==========================

FROG_ID = "frog_id"
FACTURA = "factura"
CLIENTE = "cliente"
FECHA_LIQUIDACION = "fecha_liquidacion"
FABRICANTE = "fabricante"
PREVENTA = "preventa"
REPARTO = "reparto"
DENOMINACION_COMERCIAL = "denominacion_comercial"
PRODUCTO = "producto"
DESCRIPCION_CANAL = "descripcion_canal"
MARCA = "marca"
PRESENTACION = "presentacion"
CAJAS = "cajas"
UNIDAD = "unidad"
MULTIPLO = "multiplo"
IMPORTE_BRUTO = "importe_bruto"
TOTAL = "total"
FACTOR_CONVERSION_1 = "factor_conversion_1"
FACTOR_CONVERSION_3 = "factor_conversion_3"
HLT = "hlt"
DESCRIPCION_PRODUCTO = "descripcion_producto"
PLAZA = "plaza"
CANAL = "canal"
CLASIFICACION = "clasificacion"
CF = "cf"
SABOR = "sabor"
COMPANIA = "compania"
ANIO = "anio"

# ==========================
# Mapeo CSV -> columnas internas
# ==========================

CSV_COLUMNS = {
    "FrogId a pedido\n[Pedido]": FROG_ID,
    "FACTURA": FACTURA,
    "Cliente\n[Cliente]": CLIENTE,
    "Fecha de liquidación\n[Liquidación]": FECHA_LIQUIDACION,
    "Descripción\nFabricante": FABRICANTE,
    "PREVENTA": PREVENTA,
    "REPARTO": REPARTO,
    "Denominación comercial\n[Cliente]": DENOMINACION_COMERCIAL,
    "Producto\n[Pedido det.]": PRODUCTO,
    "Descripción\nCanal": DESCRIPCION_CANAL,
    "Descripción\nMarca": MARCA,
    "Descripción\nCatalogo presentaciones": PRESENTACION,
    "CAJAS": CAJAS,
    "Unidad\n[Pedido det.]": UNIDAD,
    "Multiplica\n[Múltiplo producto]": MULTIPLO,
    " IMPORTE BRUTO S/IMP ": IMPORTE_BRUTO,
    " TOTAL S/IMP ": TOTAL,
    "Factor conversión 1\n[Producto]": FACTOR_CONVERSION_1,
    "Factor conversión 3\n[Producto]": FACTOR_CONVERSION_3,
    "HLT": HLT,
    "Descripción\n[Producto]": DESCRIPCION_PRODUCTO,
    "PLAZA": PLAZA,
    "CANAL": CANAL,
    "CLASIF": CLASIFICACION,
    "CF": CF,
    "SABOR": SABOR,
    "Compañía": COMPANIA,
    "AÑO": ANIO,
}
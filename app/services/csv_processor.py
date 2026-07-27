from pathlib import Path

import polars as pl

from app.core.csv_columns import (
    CSV_COLUMNS,
    PRODUCTO,
    FABRICANTE,
    MARCA,
    CAJAS,
)


class CsvProcessor:
    """
    Procesa el archivo CSV aplicando las reglas de negocio.
    """

    PRODUCT_RULES = {
        8007: "ENVASE",
        8008: "ENVASE",
        8009: "ENVASE",
        9955: "GARRAFON",
        9957: "GARRAFON",
        6051: "GARRAFON",
    }

    MANUFACTURER_RULES = {
        "BONAFONT S.A. DE C.V.": "BONAFONT BOTELLA",
        "ENVASADORAS DE AGUAS EN MEXICO S. DE R.L. DE C.V.": "GARRAFON",
    }

    @classmethod
    def process(cls, file_path: Path) -> pl.DataFrame:
        """
        Lee el CSV y aplica todas las reglas de negocio.
        """

        df = pl.read_csv(
            file_path,
            schema_overrides={
                "Cliente\n[Cliente]": pl.Utf8,
            },
        )

        df = cls.normalize_csv_headers(df)

        cls.validate_headers(df)

        df = cls.normalize_headers(df)

        df = cls.remove_zero_boxes(df)

        df = cls.apply_manufacturer_rules(df)

        df = cls.apply_product_rules(df)

        return df

    @classmethod
    def validate_headers(cls, df: pl.DataFrame) -> None:
        """
        Verifica que el CSV contenga todas las columnas requeridas.
        """

        expected = set(CSV_COLUMNS.keys())
        received = set(df.columns)

        missing = expected - received

        if missing:
            raise ValueError(
                "El archivo CSV no contiene todas las columnas requeridas.\n"
                f"Faltan: {', '.join(sorted(missing))}"
            )

    @classmethod
    def normalize_headers(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Renombra las columnas del CSV utilizando nombres internos.
        """

        return df.rename(CSV_COLUMNS)

    @classmethod
    def remove_zero_boxes(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Elimina los registros cuya cantidad de cajas sea igual a cero.
        """

        return df.filter(
            pl.col(CAJAS) != 0
        )

    @classmethod
    def apply_manufacturer_rules(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Aplica reglas basadas en el fabricante.
        """

        brand = pl.col(MARCA)

        for manufacturer, value in cls.MANUFACTURER_RULES.items():
            brand = (
                pl.when(pl.col(FABRICANTE) == manufacturer)
                .then(pl.lit(value))
                .otherwise(brand)
            )

        return df.with_columns(
            brand.alias(MARCA)
        )

    @classmethod
    def apply_product_rules(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Aplica reglas basadas en el producto.
        Las reglas de producto tienen prioridad sobre las de fabricante.
        """

        brand = pl.col(MARCA)

        for product, value in cls.PRODUCT_RULES.items():
            brand = (
                pl.when(pl.col(PRODUCTO) == product)
                .then(pl.lit(value))
                .otherwise(brand)
            )

        return df.with_columns(
            brand.alias(MARCA)
        )

    @classmethod
    def normalize_csv_headers(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Normaliza los encabezados del CSV eliminando diferencias de
        saltos de línea y espacios.
        """

        rename_map = {}

        for column in df.columns:
            normalized = (
                column
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .strip()
            )

            rename_map[column] = normalized

        return df.rename(rename_map)
from pathlib import Path
from app.core.csv_columns import IMPORTE_BRUTO, TOTAL

import polars as pl

from app.core.csv_columns import (
    CSV_COLUMNS,
    PRODUCTO,
    FABRICANTE,
    MARCA,
    CAJAS,
    TEXT_COLUMNS,
    INTEGER_COLUMNS,
    FLOAT_COLUMNS,
    DATE_COLUMNS,
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
            infer_schema_length=None,
        )
                
        df = cls.normalize_csv_headers(df)

        print(df.select([
            "IMPORTE BRUTO S/IMP",
            "TOTAL S/IMP"
        ]).head())

        df = cls.normalize_headers(df)

        cls.validate_headers(df)

        df = cls.cast_columns(df)

        print(
            df.select([
                IMPORTE_BRUTO,
                TOTAL,
            ]).head()
        )

        df = cls.remove_zero_boxes(df)

        df = cls.apply_manufacturer_rules(df)

        df = cls.apply_product_rules(df)

        return df

    @classmethod
    def validate_headers(cls, df: pl.DataFrame) -> None:
        """
        Verifica que el CSV contenga todas las columnas requeridas.
        """

        expected = set(CSV_COLUMNS.values())
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
    def cast_columns(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Convierte las columnas a los tipos utilizados por el sistema.
        """

        expressions = [
            *(
                pl.col(column).cast(pl.Utf8, strict=False)
                for column in TEXT_COLUMNS
            ),
            *(
                pl.col(column).cast(pl.Int64, strict=False)
                for column in INTEGER_COLUMNS
            ),
           *(
                pl.col(column)
                .cast(pl.Utf8, strict=False)
                .str.strip_chars()
                .str.replace_all(r"[$,]", "")
                .cast(pl.Float64, strict=False)
                for column in FLOAT_COLUMNS
            ),
            *(
                pl.col(column).str.to_date(strict=False)
                for column in DATE_COLUMNS
            ),
        ]

        return df.with_columns(expressions)

    @classmethod
    def remove_zero_boxes(cls, df: pl.DataFrame) -> pl.DataFrame:
        """
        Elimina los registros cuya cantidad de cajas sea igual a cero.
        """

        return df.filter(
            pl.col(CAJAS)
            .fill_null(0)
            .ne(0)
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

        rename_map = {
            column: (
                column
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .strip()
            )
            for column in df.columns
        }

        return df.rename(rename_map)
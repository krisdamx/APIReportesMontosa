import polars as pl


class DashboardAnalyticsEngine:

    METRIC_MAP = {
        "ventas": pl.col("total").sum().alias("ventas"),
        "importeBruto": pl.col("importe_bruto").sum().alias("importeBruto"),
        "hlt": pl.col("hlt").sum().alias("hlt"),
        "cf": pl.col("cf").cast(pl.Float64, strict=False).sum().alias("cf").alias("cf"),
        "cajas": pl.col("cajas").sum().alias("cajas"),
        "clientes": pl.col("cliente").n_unique().alias("clientes"),
        "pedidos": pl.col("frog_id").n_unique().alias("pedidos"),
        "productosVendidos": (
            pl.col("producto")
            .n_unique()
            .alias("productosVendidos")
        ),
    }

    GROUP_MAP = {
        "fabricante": "fabricante",
        "marca": "marca",
        "plaza": "plaza",
        "canal": "canal",
        "producto": "producto",
        "presentacion": "presentacion",
        "sabor": "sabor",
        "clasificacion": "clasificacion",
        "compania": "compania",
        "fecha": "fecha",
        "mes": "mes",
        "anio": "anio",
    }

    @staticmethod
    def prepare_dataframe(
        df: pl.DataFrame,
    ) -> pl.DataFrame:

        return df.with_columns(
            pl.col("fecha_liquidacion")
            .dt.strftime("%Y-%m-%d")
            .alias("fecha"),

            pl.col("fecha_liquidacion")
            .dt.strftime("%Y-%m")
            .alias("mes"),
        )

    @classmethod
    def _parse_metrics(
        cls,
        metrics: list[str],
    ):

        expressions = []

        for metric in metrics:

            if metric == "ticketPromedio":
                continue

            expression = cls.METRIC_MAP.get(metric)

            if expression is None:
                raise ValueError(
                    f"Métrica no soportada: {metric}"
                )

            expressions.append(expression)

        return expressions

    @classmethod
    def _parse_groupby(
        cls,
        groups: list[str],
    ):

        columns = []

        for group in groups:

            column = cls.GROUP_MAP.get(group)

            if column is None:
                raise ValueError(
                    f"Agrupación no soportada: {group}"
                )

            columns.append(column)

        return columns

    @classmethod
    def build(
        cls,
        df: pl.DataFrame,
        metrics: list[str],
        group_by: list[str],
        order_by: str | None = None,
        order: str = "desc",
        limit: int | None = None,
    ) -> pl.DataFrame:

        df = cls.prepare_dataframe(df)

        metric_expr = cls._parse_metrics(metrics)

        group_columns = cls._parse_groupby(group_by)

        result = (
            df
            .group_by(group_columns)
            .agg(metric_expr)
        )

        # Ticket promedio (caso especial)
        if "ticketPromedio" in metrics:

            result = (
                df
                .group_by(group_columns)
                .agg(
                    metric_expr + [
                        (
                            pl.col("total").sum()
                            / pl.col("frog_id").n_unique()
                        ).alias("ticketPromedio")
                    ]
                )
            )

        # Ordenamiento
        if not order_by:
            order_by = metrics[0]

        descending = order.lower() == "desc"

        result = result.sort(
            order_by,
            descending=descending,
        )

        # Top N
        if limit:

            result = result.head(limit)

        return result
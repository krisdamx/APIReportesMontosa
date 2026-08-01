from pydantic import BaseModel


# ==========================================================
# Catalogs
# ==========================================================

class CatalogOption(BaseModel):
    label: str
    value: str


class DashboardCatalogsResponse(BaseModel):
    fabricantes: list[CatalogOption]
    marcas: list[CatalogOption]
    plazas: list[CatalogOption]
    canales: list[CatalogOption]
    companias: list[CatalogOption]
    productos: list[CatalogOption]
    presentaciones: list[CatalogOption]
    sabores: list[CatalogOption]
    clasificaciones: list[CatalogOption]
    anios: list[CatalogOption]


# ==========================================================
# Summary
# ==========================================================

class DashboardSummaryResponse(BaseModel):
    ventas: float
    clientes: int
    cf: float
    hlt: float
    cajas: float
    pedidos: int
    ticketPromedio: float


# ==========================================================
# Analytics
# ==========================================================

from typing import Any


class DashboardAnalyticsMetadata(BaseModel):
    metrics: list[str]
    groupBy: list[str]
    records: int


class DashboardAnalyticsResponse(BaseModel):
    metadata: DashboardAnalyticsMetadata
    totals: dict[str, float | int]
    data: list[dict[str, Any]]
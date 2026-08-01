from pydantic import BaseModel


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
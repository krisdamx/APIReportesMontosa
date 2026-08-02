from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard_schemas import (
    DashboardCatalogsResponse,
    DashboardSummaryResponse,
    DashboardAnalyticsResponse,
)
from app.services.dashboard_service import DashboardService, DashboardRepository
from app.services.dashboard_analytics_engine import DashboardAnalyticsEngine

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/catalogs",
    response_model=DashboardCatalogsResponse,
)
def get_catalogs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService.get_catalogs(db)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_summary(
    fechaInicio: date | None = None,
    fechaFin: date | None = None,
    fabricante: str | None = None,
    marca: str | None = None,
    plaza: str | None = None,
    canal: str | None = None,
    compania: str | None = None,
    producto: str | None = None,
    presentacion: str | None = None,
    sabor: str | None = None,
    clasificacion: str | None = None,
    anio: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return DashboardService.get_summary(
        db=db,
        fecha_inicio=fechaInicio,
        fecha_fin=fechaFin,
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


@router.get(
    "/analytics",
    response_model=DashboardAnalyticsResponse,
)
def get_analytics(
    metrics: str,
    groupBy: str,
    aggregate: str = "sum",
    orderBy: str | None = None,
    order: str = "desc",
    limit: int | None = None,
    includeTotals: bool = True,

    fechaInicio: date | None = None,
    fechaFin: date | None = None,
    fabricante: str | None = None,
    marca: str | None = None,
    plaza: str | None = None,
    canal: str | None = None,
    compania: str | None = None,
    producto: str | None = None,
    presentacion: str | None = None,
    sabor: str | None = None,
    clasificacion: str | None = None,
    anio: int | None = None,

    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if aggregate != "sum":
        raise ValueError(
            "Actualmente solo se soporta aggregate=sum."
        )

    return DashboardService.get_analytics(
        db=db,
        metrics=metrics.split(","),
        group_by=groupBy.split(","),
        order_by=orderBy,
        order=order,
        limit=limit,
        include_totals=includeTotals,
        fecha_inicio=fechaInicio,
        fecha_fin=fechaFin,
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



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard_schemas import DashboardCatalogsResponse
from app.services.dashboard_service import DashboardService

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
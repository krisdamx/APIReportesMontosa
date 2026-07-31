from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.archivo_schema import ArchivoResponse, ArchivoDetailResponse
from app.services.archivo_service import ArchivoService

router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


@router.get(
    "",
    response_model=list[ArchivoResponse],
)
def get_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return ArchivoService.get_files(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/{archivo_id}",
    response_model=ArchivoDetailResponse,
)
def get_file(
    archivo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    try:

        return ArchivoService.get_file(
            db=db,
            archivo_id=archivo_id,
            user_id=current_user.id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
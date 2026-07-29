from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.upload_response import UploadResponse
from app.services.upload_service import UploadService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("", response_model=UploadResponse)
def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos CSV.",
        )

    archivo = UploadService.upload(
        file=file,
        db=db,
        user_id=current_user.id,
    )

    return UploadResponse(
        id=archivo.id,
        filename=archivo.nombre_original,
        records=archivo.total_registros,
        status=archivo.status.value,
    )
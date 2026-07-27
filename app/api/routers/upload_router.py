from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.upload_response import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("", response_model=UploadResponse)
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos CSV.",
        )

    archivo = UploadService.upload(file, db)

    return UploadResponse(
        id=archivo.id,
        filename=archivo.nombre_original,
        records=archivo.total_registros,
        status=archivo.status.value,
    )
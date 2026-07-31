from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.archivo import ImportStatus


class ArchivoResponse(BaseModel):
    id: int
    nombre_original: str
    total_registros: int
    status: ImportStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ArchivoDetailResponse(BaseModel):
    id: int
    nombre_original: str
    extension: str
    mime_type: str
    file_size: int
    total_registros: int
    processing_time_ms: int | None
    status: ImportStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
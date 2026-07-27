from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: int
    filename: str
    records: int
    status: str
from fastapi import APIRouter

from app.api.routers.health_router import router as health_router
from app.api.routers.upload_router import router as upload_router

router = APIRouter()

router.include_router(health_router)
router.include_router(upload_router)
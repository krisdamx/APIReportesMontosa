from fastapi import FastAPI

from app.api.routers import router

app = FastAPI(
    title="Sales Analytics API",
    version="1.0.0",
)

app.include_router(router)
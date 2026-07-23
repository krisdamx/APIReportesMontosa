"""
Global Exception Handlers.

Centraliza el manejo de todas las excepciones de la aplicación.

Uso:

from app.core.handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import SalesAnalyticsException
from app.core.logger import logger


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos los handlers globales.
    """

    # ==========================================================
    # Custom Exceptions
    # ==========================================================

    @app.exception_handler(SalesAnalyticsException)
    async def sales_exception_handler(
        request: Request,
        exc: SalesAnalyticsException,
    ) -> JSONResponse:

        logger.warning(
            f"{request.method} {request.url.path} | "
            f"{exc.error_code} | "
            f"{exc.message}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.__class__.__name__,
                "code": exc.error_code,
                "message": exc.message,
            },
        )

    # ==========================================================
    # FastAPI HTTP Exceptions
    # ==========================================================

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:

        logger.warning(
            f"{request.method} {request.url.path} | HTTPException | {exc.detail}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "HTTPException",
                "code": "HTTP_EXCEPTION",
                "message": exc.detail,
            },
        )

    # ==========================================================
    # Request Validation
    # ==========================================================

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:

        logger.warning(
            f"{request.method} {request.url.path} | Validation Error"
        )

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "ValidationError",
                "code": "VALIDATION_ERROR",
                "message": "La solicitud contiene datos inválidos.",
                "details": exc.errors(),
            },
        )

    # ==========================================================
    # Unknown Exceptions
    # ==========================================================

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        logger.exception(
            f"{request.method} {request.url.path}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": exc.__class__.__name__,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ocurrió un error interno en el servidor.",
            },
        )
"""
Standard API Responses.

Todas las respuestas exitosas de la API deberán utilizar
estos modelos.
"""

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Respuesta estándar para toda la API.
    """

    success: bool = True

    message: str = "Operación realizada correctamente."

    data: Optional[T] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class PaginatedResponse(ApiResponse[T]):
    """
    Respuesta para listas paginadas.
    """

    total: int

    page: int

    page_size: int


class CreatedResponse(ApiResponse[T]):
    """
    Respuesta para creación de recursos.
    """

    message: str = "Recurso creado correctamente."


class UpdatedResponse(ApiResponse[T]):
    """
    Respuesta para actualización.
    """

    message: str = "Recurso actualizado correctamente."


class DeletedResponse(ApiResponse[None]):
    """
    Respuesta para eliminación.
    """

    data: None = None

    message: str = "Recurso eliminado correctamente."s
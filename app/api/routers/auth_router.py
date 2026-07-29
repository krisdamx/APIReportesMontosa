"""
Rutas de autenticación.

Responsabilidades:
- Inicio de sesión.
- Obtener información del usuario autenticado (futuro).

La lógica de negocio se delega completamente a AuthService.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth_schemas import LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve un JWT.",
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Autentica un usuario mediante username y password.
    """

    try:
        return AuthService.login(
            db=db,
            request=request,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
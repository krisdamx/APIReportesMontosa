"""
Rutas de autenticación.

Responsabilidades:
- Inicio de sesión.
- Obtener información del usuario autenticado.

Toda la lógica de negocio se delega a AuthService y la autenticación
se resuelve mediante get_current_user.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth_schemas import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario mediante username y password y devuelve un JWT.",
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Autentica un usuario y genera un token JWT.
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


@router.post(
    "/register",
    response_model=RegisterResponse,
    summary="Registrar usuario",
    description="Crea un nuevo usuario.",
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse:

    try:

        return AuthService.register(
            db=db,
            request=request,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="Cerrar sesión",
    description="Finaliza la sesión del usuario autenticado.",
)
def logout(
    current_user: User = Depends(get_current_user),
) -> LogoutResponse:
    """
    Cierra la sesión del usuario.

    En una autenticación basada en JWT el cierre de sesión consiste en
    invalidar el token del lado del cliente eliminándolo de su almacenamiento.
    """

    return LogoutResponse(
        message="Sesión cerrada correctamente."
    )
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.services.jwt_service import JwtService
from app.services.password_service import PasswordService


class AuthService:

    @staticmethod
    def login(
        db,
        request: LoginRequest,
    ) -> LoginResponse:

        user = AuthRepository.get_by_username(
            db,
            request.username,
        )

        if user is None:
            raise ValueError("Usuario o contraseña incorrectos.")

        if not PasswordService.verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError("Usuario o contraseña incorrectos.")

        token = JwtService.create_access_token(
            user.id,
            user.username,
        )

        return LoginResponse(
            access_token=token,
            token_type="bearer",
        )

    @staticmethod
    def register(
        db,
        request: RegisterRequest,
    ) -> RegisterResponse:

        existing_user = AuthRepository.get_by_username(
            db,
            request.username,
        )

        if existing_user is not None:
            raise ValueError(
                "El nombre de usuario ya existe."
            )

        user = User(
            username=request.username,
            nombre=request.nombre,
            password_hash=PasswordService.hash_password(
                request.password,
            ),
        )

        user = AuthRepository.create_user(
            db=db,
            user=user,
        )

        return RegisterResponse(
            id=user.id,
            username=user.username,
            nombre=user.nombre,
            message="Usuario creado correctamente.",
        )
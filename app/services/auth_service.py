from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schemas import LoginRequest, LoginResponse
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
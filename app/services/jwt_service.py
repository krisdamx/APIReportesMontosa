from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings


class JwtService:

    @classmethod
    def create_access_token(
        cls,
        user_id: int,
        username: str,
    ) -> str:

        expire = datetime.now(UTC) + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES,
        )

        payload = {
            "sub": str(user_id),
            "username": username,
            "exp": expire,
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except JWTError as exc:
            raise ValueError("Token inválido o expirado.") from exc
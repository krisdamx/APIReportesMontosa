from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.services.jwt_service import JwtService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = JwtService.decode_token(token)
        username = payload.get("username")

        if username is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = AuthRepository.get_by_username(
        db=db,
        username=username,
    )

    if user is None:
        raise credentials_exception

    return user
from sqlalchemy.orm import Session

from app.models.user import User


class AuthRepository:

    @staticmethod
    def get_by_username(
        db: Session,
        username: str,
    ) -> User | None:

        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    @staticmethod
    def create_user(
        db: Session,
        user: User,
    ) -> User:

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
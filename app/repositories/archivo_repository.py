from sqlalchemy.orm import Session

from app.models.archivo import Archivo


class ArchivoRepository:

    @staticmethod
    def create(db: Session, archivo: Archivo) -> Archivo:
        db.add(archivo)
        db.commit()
        db.refresh(archivo)
        return archivo

    @staticmethod
    def update(db: Session, archivo: Archivo) -> Archivo:
        db.commit()
        db.refresh(archivo)
        return archivo

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: int,
    ) -> list[Archivo]:

        return (
            db.query(Archivo)
            .filter(
                Archivo.created_by == user_id,
                Archivo.is_active.is_(True),
            )
            .order_by(
                Archivo.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_id_and_user(
        db: Session,
        archivo_id: int,
        user_id: int,
    ) -> Archivo | None:

        return (
            db.query(Archivo)
            .filter(
                Archivo.id == archivo_id,
                Archivo.created_by == user_id,
                Archivo.is_active.is_(True),
            )
            .first()
        )
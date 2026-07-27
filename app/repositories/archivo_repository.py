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

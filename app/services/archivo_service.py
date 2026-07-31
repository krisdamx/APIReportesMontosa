from sqlalchemy.orm import Session

from app.repositories.archivo_repository import ArchivoRepository


class ArchivoService:

    @staticmethod
    def get_files(
        db: Session,
        user_id: int,
    ):
        return ArchivoRepository.get_by_user(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def get_file(
        db: Session,
        archivo_id: int,
        user_id: int,
    ):

        archivo = ArchivoRepository.get_by_id_and_user(
            db=db,
            archivo_id=archivo_id,
            user_id=user_id,
        )

        if archivo is None:
            raise ValueError("Archivo no encontrado.")

        return archivo
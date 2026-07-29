import hashlib
import logging
import shutil
import time

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import ImportStatus
from app.models.archivo import Archivo
from app.repositories.archivo_repository import ArchivoRepository
from app.repositories.venta_repository import VentaRepository
from app.services.csv_processor import CsvProcessor
from app.mappers.venta_mapper import VentaMapper

logger = logging.getLogger(__name__)


class UploadService:

    CHUNK_SIZE = 1024 * 1024  # 1 MB

    @classmethod
    def upload(
        cls,
        file: UploadFile,
        db: Session,
        user_id: int,
    ) -> Archivo:

        start = time.perf_counter()

        logger.info("Iniciando procesamiento del archivo: %s", file.filename)

        # Nombre temporal
        temp_path = settings.CSV_PATH / f"{file.filename}.tmp"

        # Copiar directamente al disco
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Calcular SHA256 por bloques
        sha256 = hashlib.sha256()

        with open(temp_path, "rb") as f:
            while chunk := f.read(cls.CHUNK_SIZE):
                sha256.update(chunk)

        file_hash = sha256.hexdigest()

        # Nombre definitivo
        final_name = f"{file_hash}.csv"
        final_path = settings.CSV_PATH / final_name

        temp_path.rename(final_path)

        file_size = final_path.stat().st_size

        try:
            df = CsvProcessor.process(final_path)

            if df.height == 0:
                raise ValueError("El archivo no contiene registros válidos.")

            total_records = df.height

            logger.info(
                "CSV leído correctamente: %s registros",
                total_records,
            )

        except Exception:
            final_path.unlink(missing_ok=True)
            raise

        archivo = Archivo(
            nombre_original=file.filename,
            nombre_storage=final_name,
            storage_path=str(final_path),
            file_hash=file_hash,
            extension=".csv",
            mime_type=file.content_type,
            file_size=file_size,
            total_registros=total_records,
            status=ImportStatus.PENDING,
            created_by=user_id,
        )

        archivo = ArchivoRepository.create(db, archivo)

        rows = VentaMapper.to_rows(
            archivo_id=archivo.id,
            created_by=user_id,
            df=df,
        )

        logger.info("Iniciando carga en base de datos...")

        total = VentaRepository.bulk_upsert(
            db=db,
            rows=rows,
        )

        elapsed = time.perf_counter() - start

        archivo.status = ImportStatus.COMPLETED
        archivo.processing_time_ms = int(elapsed * 1000)

        logger.info(
            "Carga finalizada: %s registros procesados",
            total,
        )

        logger.info(
            "Tiempo total: %.2f segundos",
            elapsed,
        )

        logger.info(
            "Archivo %s procesado correctamente",
            archivo.nombre_original,
        )

        return ArchivoRepository.update(db, archivo)
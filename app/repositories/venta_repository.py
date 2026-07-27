import logging

from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app.models.venta import Venta
from app.core.constants import BATCH_SIZE

logger = logging.getLogger(__name__)


class VentaRepository:

    @classmethod
    def bulk_upsert(
        cls,
        db: Session,
        rows: list[dict],
    ) -> int:

        if not rows:
            return 0

        total = 0

        for index, batch in enumerate(
            _chunked(rows, BATCH_SIZE),
            start=1,
        ):
            logger.info(
                "Procesando batch %s (%s registros)",
                index,
                len(batch),
            )

            stmt = insert(Venta).values(batch)

            update_columns = {
                column.name: stmt.inserted[column.name]
                for column in Venta.__table__.columns
                if column.name not in (
                    "id",
                    "business_key",
                    "created_at",
                    "created_by",
                    "updated_at",
                )
            }

            stmt = stmt.on_duplicate_key_update(**update_columns)

            db.execute(stmt)

            total += len(batch)

            logger.info(
                "Importación completada: %s registros procesados en %s batches.",
                total,
                index,
            )    

        return total

def _chunked(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]
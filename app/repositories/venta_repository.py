from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session

from app.models.venta import Venta


class VentaRepository:

    @classmethod
    def bulk_upsert(
        cls,
        db: Session,
        rows: list[dict],
    ) -> int:

        if not rows:
            return 0

        stmt = insert(Venta).values(rows)

        update_columns = {
        column.name: stmt.inserted[column.name]
        for column in Venta.__table__.columns
        if column.name not in (
            "id",
            "business_key",
            "created_at",
            "created_by",
            "updated_at",
            "is_active",
        )
    }

        stmt = stmt.on_duplicate_key_update(**update_columns)

        print(
            stmt.compile(
                dialect=db.bind.dialect,
                compile_kwargs={"literal_binds": False},
            )
        )

        db.execute(stmt)

        return len(rows)
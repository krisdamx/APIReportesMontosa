"""Initial schema

Revision ID: c3247789c958
Revises:
Create Date: 2026-07-24 20:34:37.949902
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3247789c958"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # Archivos
    # ------------------------------------------------------------------
    op.create_table(
        "archivos",
        sa.Column("nombre_original", sa.String(255), nullable=False),
        sa.Column("nombre_storage", sa.String(255), nullable=False),
        sa.Column("storage_path", sa.String(500), nullable=False),
        sa.Column("file_hash", sa.String(64), nullable=False),
        sa.Column("extension", sa.String(10), nullable=False),
        sa.Column("mime_type", sa.String(120), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("total_registros", sa.Integer(), nullable=False),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "PROCESSING",
                "COMPLETED",
                "FAILED",
                name="importstatus",
            ),
            nullable=False,
        ),
        sa.Column("error_code", sa.String(100)),
        sa.Column("error_message", sa.Text()),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_by", sa.Integer()),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_archivos_file_hash"),
        "archivos",
        ["file_hash"],
        unique=True,
    )

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    op.create_table(
        "usuarios",
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_by", sa.Integer()),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_usuarios_username"),
        "usuarios",
        ["username"],
        unique=True,
    )

    # ------------------------------------------------------------------
    # Ventas
    # ------------------------------------------------------------------
    op.create_table(
        "ventas",
        sa.Column("archivo_id", sa.Integer(), nullable=False),
        sa.Column("business_key", sa.String(64), nullable=False),
        sa.Column("frog_id", sa.String(150), nullable=False),
        sa.Column("factura", sa.String(100)),
        sa.Column("cliente", sa.String(255)),
        sa.Column("fecha_liquidacion", sa.Date()),
        sa.Column("fabricante", sa.String(150)),
        sa.Column("preventa", sa.String(150)),
        sa.Column("reparto", sa.String(150)),
        sa.Column("denominacion_comercial", sa.String(255)),
        sa.Column("producto", sa.String(255)),
        sa.Column("descripcion_canal", sa.String(150)),
        sa.Column("marca", sa.String(150)),
        sa.Column("presentacion", sa.String(150)),
        sa.Column("cajas", sa.DECIMAL(18, 4)),
        sa.Column("unidad", sa.String(50)),
        sa.Column("multiplo", sa.DECIMAL(18, 4)),
        sa.Column("importe_bruto", sa.DECIMAL(18, 4)),
        sa.Column("total", sa.DECIMAL(18, 4)),
        sa.Column("factor_conversion_1", sa.DECIMAL(18, 4)),
        sa.Column("factor_conversion_3", sa.DECIMAL(18, 4)),
        sa.Column("hlt", sa.DECIMAL(18, 4)),
        sa.Column("descripcion_producto", sa.String(255)),
        sa.Column("plaza", sa.String(100)),
        sa.Column("canal", sa.String(100)),
        sa.Column("clasificacion", sa.String(100)),
        sa.Column("cf", sa.DECIMAL(18, 6)),
        sa.Column("sabor", sa.String(100)),
        sa.Column("compania", sa.String(150)),
        sa.Column("anio", sa.SmallInteger()),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_by", sa.Integer()),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["archivo_id"],
            ["archivos.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_ventas_archivo_id"),
        "ventas",
        ["archivo_id"],
    )

    op.create_index(
        op.f("ix_ventas_business_key"),
        "ventas",
        ["business_key"],
        unique=True,
    )

    op.create_index(
        op.f("ix_ventas_frog_id"),
        "ventas",
        ["frog_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_ventas_frog_id"),
        table_name="ventas",
    )

    op.drop_index(
        op.f("ix_ventas_business_key"),
        table_name="ventas",
    )

    op.drop_index(
        op.f("ix_ventas_archivo_id"),
        table_name="ventas",
    )

    op.drop_table("ventas")

    op.drop_index(
        op.f("ix_usuarios_username"),
        table_name="usuarios",
    )

    op.drop_table("usuarios")

    op.drop_index(
        op.f("ix_archivos_file_hash"),
        table_name="archivos",
    )

    op.drop_table("archivos")
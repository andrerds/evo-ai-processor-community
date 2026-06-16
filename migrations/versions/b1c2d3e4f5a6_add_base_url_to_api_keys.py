"""add base_url to evo_core_api_keys

Revision ID: b1c2d3e4f5a6
Revises: 26a14ac7025d
Create Date: 2026-06-05 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, None] = '26a14ac7025d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add base_url column to evo_core_api_keys if missing.

    The column is mirrored from the Go core service migration 000006 so the
    processor can read it. Skipped when already present to keep the
    migration idempotent across services that may have applied the Go
    migration first.
    """
    bind = op.get_bind()
    result = bind.execute(
        sa.text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = 'evo_core_api_keys' AND column_name = 'base_url'"
        )
    ).first()
    if result is None:
        op.add_column(
            'evo_core_api_keys',
            sa.Column('base_url', sa.Text(), nullable=True),
        )


def downgrade() -> None:
    """Drop base_url column from evo_core_api_keys if present."""
    bind = op.get_bind()
    result = bind.execute(
        sa.text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = 'evo_core_api_keys' AND column_name = 'base_url'"
        )
    ).first()
    if result is not None:
        op.drop_column('evo_core_api_keys', 'base_url')

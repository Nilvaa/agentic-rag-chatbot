"""add conversation timestamp defaults

Revision ID: d78e06050a6a
Revises: 0c16177610bd
Create Date: 2026-08-22 15:04:41.221066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd78e06050a6a'
down_revision: Union[str, Sequence[str], None] = '0c16177610bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "conversations",
        "created_at",
        server_default=sa.text("now()")
    )

    op.alter_column(
        "conversations",
        "updated_at",
        server_default=sa.text("now()")
    )


def downgrade() -> None:
    op.alter_column(
        "conversations",
        "created_at",
        server_default=None
    )

    op.alter_column(
        "conversations",
        "updated_at",
        server_default=None
    )
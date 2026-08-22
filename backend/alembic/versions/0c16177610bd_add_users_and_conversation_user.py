"""add users and conversation user

Revision ID: 0c16177610bd
Revises: 16a9587f5f24
Create Date: 2026-08-22 11:30:57.897729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0c16177610bd'
down_revision: Union[str, Sequence[str], None] = '16a9587f5f24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add user_id temporarily as nullable because
    # existing conversations do not have a user yet.
    op.add_column(
        "conversations",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True
        )
    )

    # Connect conversations to users
    op.create_foreign_key(
        "fk_conversations_user_id",
        "conversations",
        "users",
        ["user_id"],
        ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "fk_conversations_user_id",
        "conversations",
        type_="foreignkey"
    )

    op.drop_column(
        "conversations",
        "user_id"
    )

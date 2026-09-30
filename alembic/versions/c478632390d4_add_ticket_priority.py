"""add ticket priority

Revision ID: c478632390d4
Revises: d1f9d42fae84
Create Date: 2026-09-30 15:21:08.185528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c478632390d4'
down_revision: Union[str, Sequence[str], None] = 'd1f9d42fae84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tickets",
        sa.Column("priority", sa.String(), nullable=True)
    )

    op.execute(
        "UPDATE tickets SET priority = 'medium' WHERE priority IS NULL"
    )

    op.alter_column(
        "tickets",
        "priority",
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tickets", "priority")

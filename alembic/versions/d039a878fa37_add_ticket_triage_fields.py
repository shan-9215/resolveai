"""add ticket triage fields

Revision ID: d039a878fa37
Revises: c478632390d4
Create Date: 2026-10-02 16:00:16.249864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd039a878fa37'
down_revision: Union[str, Sequence[str], None] = 'c478632390d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tickets",
        sa.Column("category", sa.String(), nullable=True)
    )
    op.add_column(
        "tickets",
        sa.Column("impact", sa.String(), nullable=True)
    )
    op.add_column(
        "tickets",
        sa.Column("urgency", sa.String(), nullable=True)
    )
    op.add_column(
        "tickets",
        sa.Column("ai_summary", sa.String(), nullable=True)
    )
    op.add_column(
        "tickets",
        sa.Column("ai_confidence", sa.Float(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tickets", "ai_confidence")
    op.drop_column("tickets", "ai_summary")
    op.drop_column("tickets", "urgency")
    op.drop_column("tickets", "impact")
    op.drop_column("tickets", "category")

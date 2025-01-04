"""create table email_events

Revision ID: a63a0a21d301
Revises: 7d9ab2d53b40
Create Date: 2025-01-04 06:06:01.325472

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a63a0a21d301"
down_revision: Union[str, None] = "7d9ab2d53b40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "email_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email_id", sa.Uuid(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event", sa.String(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(
            ["email_id"],
            ["emails.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.Index("email_events_by_email_idx", "email_id", "id", unique=True),
    )


def downgrade() -> None:
    op.drop_table("email_events", if_exists=True)

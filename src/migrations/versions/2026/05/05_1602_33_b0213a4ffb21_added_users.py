"""added users

Revision ID: b0213a4ffb21
Revises: 125ee2cc1822
Create Date: 2026-05-05 16:02:33.716891

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "b0213a4ffb21"
down_revision: Union[str, Sequence[str], None] = "125ee2cc1822"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")

"""make email unique

Revision ID: 7af818840961
Revises: b1aa6d052032
Create Date: 2026-05-07 16:05:10.590011

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "7af818840961"
down_revision: Union[str, Sequence[str], None] = "b1aa6d052032"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")


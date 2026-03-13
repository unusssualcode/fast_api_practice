"""added rooms

Revision ID: 6ef0ebaee8c4
Revises: 125ee2cc1822
Create Date: 2026-03-13 16:36:05.656146

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6ef0ebaee8c4"
down_revision: Union[str, Sequence[str], None] = "125ee2cc1822"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

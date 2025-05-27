"""remove_post_title_column

Revision ID: f646dd76ee86
Revises: 6205cfde0885
Create Date: 2025-05-25 21:33:52.088264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f646dd76ee86'
down_revision: Union[str, None] = '6205cfde0885'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""make_post_title_nullable

Revision ID: 6205cfde0885
Revises: c2c48952a8e2
Create Date: 2025-05-25 00:31:05.155402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6205cfde0885'
down_revision: Union[str, None] = 'c2c48952a8e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Make post title column nullable
    op.alter_column('post', 'title', 
                    existing_type=sa.String(), 
                    nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert post title column to non-nullable
    op.alter_column('post', 'title', 
                    existing_type=sa.String(), 
                    nullable=False)

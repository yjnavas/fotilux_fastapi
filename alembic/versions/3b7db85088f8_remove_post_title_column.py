"""remove_post_title_column

Revision ID: 3b7db85088f8
Revises: f646dd76ee86
Create Date: 2025-05-25 21:34:15.744819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b7db85088f8'
down_revision: Union[str, None] = 'f646dd76ee86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove title column from post table
    op.drop_column('post', 'title')


def downgrade() -> None:
    """Downgrade schema."""
    # Add title column back to post table
    op.add_column('post', sa.Column('title', sa.String(), nullable=True))

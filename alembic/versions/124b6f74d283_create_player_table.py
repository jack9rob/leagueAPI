"""create player table

Revision ID: 124b6f74d283
Revises: 
Create Date: 2023-11-21 16:03:42.921191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import TIMESTAMP, func

from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '124b6f74d283'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'players',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('firstname', sa.String, nullable=False),
        sa.Column('lastname', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('is_admin', sa.Boolean, nullable=False, server_default=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=func.now())
    )
    pass


def downgrade() -> None:
    op.drop_table('players')
    pass

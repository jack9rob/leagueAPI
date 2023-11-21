"""create address table

Revision ID: 2abf548d1d52
Revises: 124b6f74d283
Create Date: 2023-11-21 16:06:55.717472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision: str = '2abf548d1d52'
down_revision: Union[str, None] = '124b6f74d283'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('city', sa.String, nullable=False),
        sa.Column('street', sa.String, nullable=False),
        sa.Column('apartment_number', sa.Integer, nullable=True),
        sa.Column('postal_code', sa.String, nullable=False),
        sa.Column('player_id', sa.Integer, ForeignKey('players.id', ondelete="CASCADE"), nullable=False, ),
        )
    pass


def downgrade() -> None:
    op.drop_table('addresses')
    pass

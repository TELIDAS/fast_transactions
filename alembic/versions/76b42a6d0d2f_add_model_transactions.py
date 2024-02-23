"""add model transactions

Revision ID: 76b42a6d0d2f
Revises: 
Create Date: 2024-02-23 18:23:56.686648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76b42a6d0d2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('base', sa.String(), nullable=True),
    sa.Column('created_datetime', sa.DateTime(), nullable=True),
    sa.Column('updated_datetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exchange_rates_id'), 'exchange_rates', ['id'], unique=False)
    op.create_table('currency_rates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency_code', sa.String(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('exchange_rate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exchange_rate_id'], ['exchange_rates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_currency_rates_currency_code'), 'currency_rates', ['currency_code'], unique=False)
    op.create_index(op.f('ix_currency_rates_id'), 'currency_rates', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_currency_rates_id'), table_name='currency_rates')
    op.drop_index(op.f('ix_currency_rates_currency_code'), table_name='currency_rates')
    op.drop_table('currency_rates')
    op.drop_index(op.f('ix_exchange_rates_id'), table_name='exchange_rates')
    op.drop_table('exchange_rates')
    # ### end Alembic commands ###

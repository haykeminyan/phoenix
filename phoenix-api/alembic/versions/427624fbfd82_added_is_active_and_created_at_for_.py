"""added is_active and created_at for model User

Revision ID: 427624fbfd82
Revises:
Create Date: 2024-02-06 11:21:53.222663

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '427624fbfd82'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_date', sa.Date(), nullable=True),
        sa.Column('created_time', sa.Time(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table(
        'apartments_rent',
        sa.Column('rent_price', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('living_area', sa.Integer(), nullable=True),
        sa.Column('number_of_bedrooms', sa.Integer(), nullable=True),
        sa.Column('number_of_bathrooms', sa.Integer(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('condition', sa.Text(), nullable=True),
        sa.Column('energy_label', sa.Text(), nullable=True),
        sa.Column('building_year', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_apartments_rent_id'), 'apartments_rent', ['id'], unique=False)
    op.create_table(
        'apartments_sale',
        sa.Column('sale_price', sa.Integer(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('living_area', sa.Integer(), nullable=True),
        sa.Column('number_of_bedrooms', sa.Integer(), nullable=True),
        sa.Column('number_of_bathrooms', sa.Integer(), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('condition', sa.Text(), nullable=True),
        sa.Column('energy_label', sa.Text(), nullable=True),
        sa.Column('building_year', sa.Integer(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_apartments_sale_id'), 'apartments_sale', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_apartments_sale_id'), table_name='apartments_sale')
    op.drop_table('apartments_sale')
    op.drop_index(op.f('ix_apartments_rent_id'), table_name='apartments_rent')
    op.drop_table('apartments_rent')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

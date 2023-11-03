"""initial

Revision ID: e04a7c7acf24
Revises: 
Create Date: 2023-11-03 20:18:09.502929

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e04a7c7acf24'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('user', 'admin', native_enum=False), server_default='user', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('adverts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('ad_type', sa.Enum('Покупка', 'Продажа', 'Оказание услуг', native_enum=False), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc',now())"), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_adverts_description'), 'adverts', ['description'], unique=False)
    op.create_index(op.f('ix_adverts_id'), 'adverts', ['id'], unique=False)
    op.create_index(op.f('ix_adverts_title'), 'adverts', ['title'], unique=False)
    op.create_table('Complaints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('advert_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc',now())"), nullable=False),
    sa.ForeignKeyConstraint(['advert_id'], ['adverts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Complaints')
    op.drop_index(op.f('ix_adverts_title'), table_name='adverts')
    op.drop_index(op.f('ix_adverts_id'), table_name='adverts')
    op.drop_index(op.f('ix_adverts_description'), table_name='adverts')
    op.drop_table('adverts')
    op.drop_table('users')
    # ### end Alembic commands ###
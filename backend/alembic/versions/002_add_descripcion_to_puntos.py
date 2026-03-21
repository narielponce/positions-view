"""add descripcion to puntos

Revision ID: 002
Revises: 001
Create Date: 2026-03-20

"""
from alembic import op
import sqlalchemy as sa


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('puntos', sa.Column('descripcion', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('puntos', 'descripcion')

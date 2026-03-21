"""initial migration

Revision ID: 001
Revises: 
Create Date: 2026-03-19

"""
from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'planos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('imagen_url', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_planos_id'), 'planos', ['id'], unique=False)

    op.create_table(
        'puntos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plano_id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('tipo', sa.String(), nullable=False),
        sa.Column('x', sa.Float(), nullable=False),
        sa.Column('y', sa.Float(), nullable=False),
        sa.Column('extra_data', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['plano_id'], ['planos.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_puntos_id'), 'puntos', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_puntos_id'), table_name='puntos')
    op.drop_table('puntos')
    op.drop_index(op.f('ix_planos_id'), table_name='planos')
    op.drop_table('planos')

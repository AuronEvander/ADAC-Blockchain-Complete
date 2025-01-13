"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-13
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    # Create blocks table
    op.create_table(
        'blocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hash', sa.String(), nullable=False),
        sa.Column('previous_hash', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('nonce', sa.Integer(), nullable=False),
        sa.Column('difficulty', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hash')
    )

    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hash', sa.String(), nullable=False),
        sa.Column('sender', sa.String(), nullable=False),
        sa.Column('recipient', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('block_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hash')
    )

def downgrade():
    op.drop_table('transactions')
    op.drop_table('blocks')
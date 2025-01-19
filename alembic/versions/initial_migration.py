"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-01-19

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create blocks table
    op.create_table('blocks',
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
    op.create_table('transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hash', sa.String(), nullable=False),
        sa.Column('from_address', sa.String(), nullable=False),
        sa.Column('to_address', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('block_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hash')
    )
    
    # Create accounts table
    op.create_table('accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=True),
        sa.Column('nonce', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('address')
    )

def downgrade():
    op.drop_table('transactions')
    op.drop_table('accounts')
    op.drop_table('blocks')
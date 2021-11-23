"""create articles table

Revision ID: e50db81c1261
Revises: 
Create Date: 2021-11-21 14:26:02.686696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e50db81c1261'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Unicode(400)),
    )


def downgrade():
    op.drop_table('articles')

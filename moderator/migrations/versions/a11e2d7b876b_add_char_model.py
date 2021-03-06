"""add char model

Revision ID: a11e2d7b876b
Revises: 0a5ad1d40108
Create Date: 2020-06-05 16:33:36.117222

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a11e2d7b876b'
down_revision = '0a5ad1d40108'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_chat',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('chat_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=80), nullable=False),
                    sa.Column('status', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('chat_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('telegram_chat')
    # ### end Alembic commands ###

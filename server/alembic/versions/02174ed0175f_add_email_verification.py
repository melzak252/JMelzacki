"""Add email verification

Revision ID: 02174ed0175f
Revises: f5a7fabc115d
Create Date: 2024-09-05 03:37:34.094936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02174ed0175f'
down_revision: Union[str, None] = 'f5a7fabc115d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sent_emails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipient', sa.String(length=255), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sent_emails_id'), 'sent_emails', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'verified')
    op.drop_index(op.f('ix_sent_emails_id'), table_name='sent_emails')
    op.drop_table('sent_emails')
    # ### end Alembic commands ###

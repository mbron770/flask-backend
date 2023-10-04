"""message

Revision ID: 72e6de81dbf1
Revises: 
Create Date: 2023-10-04 16:04:49.454040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72e6de81dbf1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
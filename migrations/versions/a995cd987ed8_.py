"""empty message

Revision ID: a995cd987ed8
Revises: fb63b87fb517
Create Date: 2021-08-30 12:55:39.446176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a995cd987ed8'
down_revision = 'fb63b87fb517'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pago', sa.Column('nroConfirmacion', sa.String(length=15), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pago', 'nroConfirmacion')
    # ### end Alembic commands ###
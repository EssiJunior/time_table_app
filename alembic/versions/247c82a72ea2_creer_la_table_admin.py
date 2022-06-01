"""creer la table admin

Revision ID: 247c82a72ea2
Revises: 
Create Date: 2022-05-31 15:11:00.903862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '247c82a72ea2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("admin",
                    sa.Column("login", sa.String(50), nullable= False, primary_key= True),
                    sa.Column("mot_de_passe", sa.String(100), nullable= False)
                    )


def downgrade():
    op.drop_table("admin")

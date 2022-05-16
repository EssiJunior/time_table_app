"""ajouter des atributs a la table activite

Revision ID: 4a1aa69a57cd
Revises: 
Create Date: 2022-05-15 20:22:39.663170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1aa69a57cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("activite", sa.Column("heure_debut", sa.Time(), nullable=False))
    op.add_column("activite", sa.Column("heure_fin", sa.Time(), nullable=False))
    op.create_foreign_key("activite_plage_horaire_fk", source_table="activite", referent_table="plage_horaire",
    local_cols=["heure_debut"], remote_cols=["heure_debut"], ondelete="CASCADE")
    op.create_foreign_key("activite_plage_horaire_fk", source_table="activite", referent_table="plage_horaire",
    local_cols=["heure_fin"], remote_cols=["heure_debut"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_column("posts", "heure_debut")
    op.drop_column("posts", "heure_fin")
    pass

"""onupdate constraint added

Revision ID: b28580ea7fe2
Revises: da49723b448c
Create Date: 2022-06-02 12:29:22.418811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b28580ea7fe2'
down_revision = 'da49723b448c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('activite_matricule_enseignant_fkey', 'activite', type_='foreignkey')
    op.drop_constraint('activite_code_salle_fkey', 'activite', type_='foreignkey')
    op.drop_constraint('activite_nom_jour_fkey', 'activite', type_='foreignkey')
    op.drop_constraint('activite_id_plage_fkey', 'activite', type_='foreignkey')
    op.create_foreign_key(None, 'activite', 'enseignant', ['matricule_enseignant'], ['matricule'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'activite', 'salle', ['code_salle'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'activite', 'plage_horaire', ['id_plage'], ['id_plage'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'activite', 'jour', ['nom_jour'], ['nom'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('classe_niveau_fkey', 'classe', type_='foreignkey')
    op.drop_constraint('classe_code_filiere_fkey', 'classe', type_='foreignkey')
    op.create_foreign_key(None, 'classe', 'filiere', ['code_filiere'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'classe', 'niveau', ['niveau'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('cours_matricule_enseignant_fkey', 'cours', type_='foreignkey')
    op.drop_constraint('cours_nom_seance_fkey', 'cours', type_='foreignkey')
    op.drop_constraint('cours_code_filiere_fkey', 'cours', type_='foreignkey')
    op.drop_constraint('cours_code_classe_fkey', 'cours', type_='foreignkey')
    op.drop_constraint('cours_id_specialite_fkey', 'cours', type_='foreignkey')
    op.create_foreign_key(None, 'cours', 'type_seance', ['nom_seance'], ['nom'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'cours', 'enseignant', ['matricule_enseignant'], ['matricule'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'cours', 'classe', ['code_classe'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'cours', 'filiere', ['code_filiere'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'cours', 'specialite', ['id_specialite'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('enseignant_code_filiere_fkey', 'enseignant', type_='foreignkey')
    op.create_foreign_key(None, 'enseignant', 'filiere', ['code_filiere'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('programmer_id_plage_fkey', 'programmer', type_='foreignkey')
    op.drop_constraint('programmer_code_cours_fkey', 'programmer', type_='foreignkey')
    op.drop_constraint('programmer_nom_jour_fkey', 'programmer', type_='foreignkey')
    op.drop_constraint('programmer_code_salle_fkey', 'programmer', type_='foreignkey')
    op.create_foreign_key(None, 'programmer', 'salle', ['code_salle'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'programmer', 'cours', ['code_cours'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'programmer', 'plage_horaire', ['id_plage'], ['id_plage'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'programmer', 'jour', ['nom_jour'], ['nom'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('specialite_code_classe_fkey', 'specialite', type_='foreignkey')
    op.create_foreign_key(None, 'specialite', 'classe', ['code_classe'], ['code'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'specialite', type_='foreignkey')
    op.create_foreign_key('specialite_code_classe_fkey', 'specialite', 'classe', ['code_classe'], ['code'], ondelete='CASCADE')
    op.drop_constraint(None, 'programmer', type_='foreignkey')
    op.drop_constraint(None, 'programmer', type_='foreignkey')
    op.drop_constraint(None, 'programmer', type_='foreignkey')
    op.drop_constraint(None, 'programmer', type_='foreignkey')
    op.create_foreign_key('programmer_code_salle_fkey', 'programmer', 'salle', ['code_salle'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('programmer_nom_jour_fkey', 'programmer', 'jour', ['nom_jour'], ['nom'], ondelete='CASCADE')
    op.create_foreign_key('programmer_code_cours_fkey', 'programmer', 'cours', ['code_cours'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('programmer_id_plage_fkey', 'programmer', 'plage_horaire', ['id_plage'], ['id_plage'], ondelete='CASCADE')
    op.drop_constraint(None, 'enseignant', type_='foreignkey')
    op.create_foreign_key('enseignant_code_filiere_fkey', 'enseignant', 'filiere', ['code_filiere'], ['code'], ondelete='CASCADE')
    op.drop_constraint(None, 'cours', type_='foreignkey')
    op.drop_constraint(None, 'cours', type_='foreignkey')
    op.drop_constraint(None, 'cours', type_='foreignkey')
    op.drop_constraint(None, 'cours', type_='foreignkey')
    op.drop_constraint(None, 'cours', type_='foreignkey')
    op.create_foreign_key('cours_id_specialite_fkey', 'cours', 'specialite', ['id_specialite'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('cours_code_classe_fkey', 'cours', 'classe', ['code_classe'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('cours_code_filiere_fkey', 'cours', 'filiere', ['code_filiere'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('cours_nom_seance_fkey', 'cours', 'type_seance', ['nom_seance'], ['nom'], ondelete='CASCADE')
    op.create_foreign_key('cours_matricule_enseignant_fkey', 'cours', 'enseignant', ['matricule_enseignant'], ['matricule'], ondelete='CASCADE')
    op.drop_constraint(None, 'classe', type_='foreignkey')
    op.drop_constraint(None, 'classe', type_='foreignkey')
    op.create_foreign_key('classe_code_filiere_fkey', 'classe', 'filiere', ['code_filiere'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('classe_niveau_fkey', 'classe', 'niveau', ['niveau'], ['code'], ondelete='CASCADE')
    op.drop_constraint(None, 'activite', type_='foreignkey')
    op.drop_constraint(None, 'activite', type_='foreignkey')
    op.drop_constraint(None, 'activite', type_='foreignkey')
    op.drop_constraint(None, 'activite', type_='foreignkey')
    op.create_foreign_key('activite_id_plage_fkey', 'activite', 'plage_horaire', ['id_plage'], ['id_plage'], ondelete='CASCADE')
    op.create_foreign_key('activite_nom_jour_fkey', 'activite', 'jour', ['nom_jour'], ['nom'], ondelete='CASCADE')
    op.create_foreign_key('activite_code_salle_fkey', 'activite', 'salle', ['code_salle'], ['code'], ondelete='CASCADE')
    op.create_foreign_key('activite_matricule_enseignant_fkey', 'activite', 'enseignant', ['matricule_enseignant'], ['matricule'], ondelete='CASCADE')
    # ### end Alembic commands ###
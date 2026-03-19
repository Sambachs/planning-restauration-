from app import create_app, db
from app.models import User, Post, Shift, Absence
import bcrypt

app = create_app()

def init_db():
    """Initialise la base de données avec des données de départ"""
    with app.app_context():
        # Crée toutes les tables
        db.create_all()

        # Crée les postes de base si ils n'existent pas
        if Post.query.count() == 0:
            postes = [
                Post(nom='Serveur', couleur='#3498db'),
                Post(nom='Cuisinier', couleur='#e67e22'),
                Post(nom='Hôte/Hôtesse', couleur='#9b59b6'),
                Post(nom='Bar', couleur='#1abc9c'),
                Post(nom='Caisse', couleur='#e74c3c'),
            ]
            db.session.add_all(postes)
            db.session.commit()
            print("✅ Postes créés")

        # Crée un manager par défaut si il n'existe pas
        if User.query.count() == 0:
            mot_de_passe = bcrypt.hashpw(
                'admin123'.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            manager = User(
                nom='Admin',
                prenom='Manager',
                email='manager@resto.fr',
                mot_de_passe=mot_de_passe,
                role='manager',
                type_contrat='CDI',
                est_actif=True
            )
            db.session.add(manager)
            db.session.commit()
            print("✅ Manager créé : manager@resto.fr / admin123")

if __name__ == '__main__':
    init_db()
    print("🚀 Lancement de l'application...")
    app.run(debug=True)
    
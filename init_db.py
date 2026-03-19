from datetime import date
from app import create_app, db
from app.models import Post, User

POSTES_PAR_DEFAUT = [
    {'nom': 'Serveur',      'couleur': '#2196F3', 'description': 'Service en salle'},
    {'nom': 'Cuisinier',    'couleur': '#FF5722', 'description': 'Préparation des plats en cuisine'},
    {'nom': 'Hôte/Hôtesse', 'couleur': '#9C27B0', 'description': 'Accueil et placement des clients'},
    {'nom': 'Bar',          'couleur': '#4CAF50', 'description': 'Service au bar'},
    {'nom': 'Caisse',       'couleur': '#FFC107', 'description': 'Encaissement et facturation'},
]

MANAGER_TEST = {
    'nom': 'Admin',
    'prenom': 'Manager',
    'email': 'admin@restaurant.fr',
    'password': 'Admin1234',
    'contrat': 'CDI',
    'date_embauche': date(2024, 1, 1),
    'role': 'manager',
}


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Tables créées.')

        for data in POSTES_PAR_DEFAUT:
            if not Post.query.filter_by(nom=data['nom']).first():
                db.session.add(Post(**data))
        db.session.commit()
        print(f'{len(POSTES_PAR_DEFAUT)} postes insérés.')

        if not User.query.filter_by(email=MANAGER_TEST['email']).first():
            manager = User(
                nom=MANAGER_TEST['nom'],
                prenom=MANAGER_TEST['prenom'],
                email=MANAGER_TEST['email'],
                contrat=MANAGER_TEST['contrat'],
                date_embauche=MANAGER_TEST['date_embauche'],
                role=MANAGER_TEST['role'],
            )
            manager.set_password(MANAGER_TEST['password'])
            db.session.add(manager)
            db.session.commit()
            print(f"Compte manager créé : {MANAGER_TEST['email']} / {MANAGER_TEST['password']}")
        else:
            print(f"Compte manager déjà existant : {MANAGER_TEST['email']}")


if __name__ == '__main__':
    init_db()

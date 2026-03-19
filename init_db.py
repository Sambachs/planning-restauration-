from datetime import date, time, timedelta
from app import create_app, db
from app.models import Post, User, Shift, Absence

POSTES_PAR_DEFAUT = [
    {'nom': 'Serveur',      'couleur': '#2196F3', 'description': 'Service en salle'},
    {'nom': 'Cuisinier',    'couleur': '#FF5722', 'description': 'Préparation des plats en cuisine'},
    {'nom': 'Hôte/Hôtesse', 'couleur': '#9C27B0', 'description': 'Accueil et placement des clients'},
    {'nom': 'Bar',          'couleur': '#4CAF50', 'description': 'Service au bar'},
    {'nom': 'Caisse',       'couleur': '#FFC107', 'description': 'Encaissement et facturation'},
]

MANAGER_TEST = {
    'nom': 'Dupont',
    'prenom': 'Marc',
    'email': 'admin@restaurant.fr',
    'password': 'Admin1234',
    'contrat': 'CDI',
    'date_embauche': date(2022, 3, 1),
    'role': 'manager',
}

EMPLOYES_MOCK = [
    {'nom': 'Martin',   'prenom': 'Sophie',  'email': 'sophie.martin@restaurant.fr',  'password': 'Employe1234', 'poste': 'Serveur',      'contrat': 'CDI',   'date_embauche': date(2023, 6, 15)},
    {'nom': 'Bernard',  'prenom': 'Lucas',   'email': 'lucas.bernard@restaurant.fr',  'password': 'Employe1234', 'poste': 'Cuisinier',    'contrat': 'CDI',   'date_embauche': date(2022, 9, 1)},
    {'nom': 'Leroy',    'prenom': 'Emma',    'email': 'emma.leroy@restaurant.fr',     'password': 'Employe1234', 'poste': 'Hôte/Hôtesse', 'contrat': 'CDD',   'date_embauche': date(2024, 1, 10)},
    {'nom': 'Moreau',   'prenom': 'Thomas',  'email': 'thomas.moreau@restaurant.fr',  'password': 'Employe1234', 'poste': 'Bar',          'contrat': 'CDI',   'date_embauche': date(2023, 3, 20)},
    {'nom': 'Petit',    'prenom': 'Camille', 'email': 'camille.petit@restaurant.fr',  'password': 'Employe1234', 'poste': 'Serveur',      'contrat': 'Extra', 'date_embauche': date(2024, 11, 5)},
    {'nom': 'Garnier',  'prenom': 'Hugo',    'email': 'hugo.garnier@restaurant.fr',   'password': 'Employe1234', 'poste': 'Cuisinier',    'contrat': 'CDI',   'date_embauche': date(2021, 7, 12)},
]


def lundi_semaine():
    today = date.today()
    return today - timedelta(days=today.weekday())


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Tables créées.')

        # Postes
        for data in POSTES_PAR_DEFAUT:
            if not Post.query.filter_by(nom=data['nom']).first():
                db.session.add(Post(**data))
        db.session.commit()
        print(f'{len(POSTES_PAR_DEFAUT)} postes insérés.')

        # Manager
        manager = User.query.filter_by(email=MANAGER_TEST['email']).first()
        if not manager:
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
            print(f"Manager : {MANAGER_TEST['email']} / {MANAGER_TEST['password']}")
        else:
            print(f"Manager déjà existant : {MANAGER_TEST['email']}")

        # Employés mock
        employes_crees = 0
        for data in EMPLOYES_MOCK:
            if not User.query.filter_by(email=data['email']).first():
                poste = Post.query.filter_by(nom=data['poste']).first()
                employe = User(
                    nom=data['nom'],
                    prenom=data['prenom'],
                    email=data['email'],
                    contrat=data['contrat'],
                    date_embauche=data['date_embauche'],
                    role='employe',
                    post_id=poste.id if poste else None,
                )
                employe.set_password(data['password'])
                db.session.add(employe)
                employes_crees += 1
        db.session.commit()
        print(f'{employes_crees} employés mock créés (mot de passe : Employe1234).')

        # Créneaux mock — semaine en cours
        if Shift.query.count() == 0:
            lundi = lundi_semaine()
            employes = User.query.filter_by(role='employe', actif=True).all()
            postes = {p.nom: p for p in Post.query.all()}

            creneaux = [
                # Lundi
                (employes[0], lundi,              time(11, 0), time(15, 30), 'Serveur'),
                (employes[1], lundi,              time(9, 0),  time(17, 0),  'Cuisinier'),
                (employes[2], lundi,              time(11, 0), time(14, 0),  'Hôte/Hôtesse'),
                # Mardi
                (employes[0], lundi + timedelta(1), time(18, 0), time(23, 0), 'Serveur'),
                (employes[1], lundi + timedelta(1), time(9, 0),  time(17, 0), 'Cuisinier'),
                (employes[3], lundi + timedelta(1), time(17, 0), time(23, 30),'Bar'),
                # Mercredi
                (employes[4], lundi + timedelta(2), time(11, 0), time(16, 0), 'Serveur'),
                (employes[1], lundi + timedelta(2), time(9, 0),  time(15, 0), 'Cuisinier'),
                (employes[5], lundi + timedelta(2), time(10, 0), time(17, 0), 'Cuisinier'),
                # Jeudi
                (employes[0], lundi + timedelta(3), time(11, 0), time(15, 30),'Serveur'),
                (employes[3], lundi + timedelta(3), time(17, 0), time(23, 30),'Bar'),
                # Vendredi
                (employes[4], lundi + timedelta(4), time(11, 0), time(16, 0), 'Serveur'),
                (employes[2], lundi + timedelta(4), time(11, 0), time(14, 0), 'Hôte/Hôtesse'),
                (employes[5], lundi + timedelta(4), time(9, 0),  time(17, 0), 'Cuisinier'),
                # Samedi
                (employes[0], lundi + timedelta(5), time(11, 0), time(23, 0), 'Serveur'),
                (employes[3], lundi + timedelta(5), time(11, 0), time(23, 30),'Bar'),
                (employes[1], lundi + timedelta(5), time(9, 0),  time(23, 0), 'Cuisinier'),
                (employes[4], lundi + timedelta(5), time(11, 0), time(16, 0), 'Serveur'),
                # Dimanche
                (employes[5], lundi + timedelta(6), time(10, 0), time(17, 0), 'Cuisinier'),
                (employes[2], lundi + timedelta(6), time(11, 0), time(15, 0), 'Hôte/Hôtesse'),
            ]

            for employe, jour, hdebut, hfin, nom_poste in creneaux:
                poste = postes.get(nom_poste)
                shift = Shift(
                    user_id=employe.id,
                    post_id=poste.id,
                    date_service=jour,
                    heure_debut=hdebut,
                    heure_fin=hfin,
                    created_by=manager.id,
                )
                db.session.add(shift)
            db.session.commit()
            print(f'{len(creneaux)} créneaux mock créés pour la semaine du {lundi}.')

        # Absences mock
        if Absence.query.count() == 0:
            employes = User.query.filter_by(role='employe', actif=True).all()
            absences = [
                Absence(user_id=employes[0].id, type_absence='conge_paye',  date_debut=date.today() + timedelta(7),  date_fin=date.today() + timedelta(11), motif='Vacances en famille',   statut='en_attente'),
                Absence(user_id=employes[2].id, type_absence='sans_solde',  date_debut=date.today() + timedelta(14), date_fin=date.today() + timedelta(15), motif='Rendez-vous personnel',  statut='approuve', traite_par=manager.id),
                Absence(user_id=employes[3].id, type_absence='maladie',     date_debut=date.today() - timedelta(2),  date_fin=date.today(),                 motif='Grippe',                statut='confirme', traite_par=manager.id),
                Absence(user_id=employes[1].id, type_absence='conge_paye',  date_debut=date.today() + timedelta(21), date_fin=date.today() + timedelta(25), motif='Congés annuels',        statut='refuse',   traite_par=manager.id, commentaire_manager='Période trop chargée.'),
            ]
            for a in absences:
                db.session.add(a)
            db.session.commit()
            print(f'{len(absences)} absences mock créées.')


if __name__ == '__main__':
    init_db()

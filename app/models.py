from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Table des utilisateurs (employés et managers)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(200), nullable=False)
    telephone = db.Column(db.String(20))
    type_contrat = db.Column(db.String(50))
    date_embauche = db.Column(db.Date)
    role = db.Column(db.String(20), nullable=False, default='employe')
    est_actif = db.Column(db.Boolean, default=True)

    # Liens vers les autres tables
    shifts = db.relationship('Shift', backref='employe', lazy=True)
    absences = db.relationship('Absence', backref='employe', lazy=True)

    def __repr__(self):
        return f'<User {self.prenom} {self.nom}>'

# Table des postes
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    couleur = db.Column(db.String(20), default='#3498db')

    shifts = db.relationship('Shift', backref='poste', lazy=True)

    def __repr__(self):
        return f'<Post {self.nom}>'

# Table des créneaux de travail
class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f'<Shift {self.date} {self.heure_debut}-{self.heure_fin}>'

# Table des absences et congés
class Absence(db.Model):
    __tablename__ = 'absences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    motif = db.Column(db.String(200))
    type_absence = db.Column(db.String(50), default='conge')
    statut = db.Column(db.String(20), default='en_attente')
    commentaire_manager = db.Column(db.Text)
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Absence {self.date_debut} - {self.date_fin}>'
        
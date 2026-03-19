from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False, unique=True)
    couleur = db.Column(db.String(7), nullable=False)
    description = db.Column(db.Text, nullable=True)

    employes = db.relationship('User', backref='poste', lazy=True)
    shifts = db.relationship('Shift', backref='poste', lazy=True)

    def __repr__(self):
        return f'<Post {self.nom}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    contrat = db.Column(db.String(20), nullable=False)
    date_embauche = db.Column(db.Date, nullable=False)
    role = db.Column(db.String(10), nullable=False, default='employe')
    actif = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    shifts = db.relationship('Shift', foreign_keys='Shift.user_id', backref='employe', lazy=True)
    absences = db.relationship('Absence', foreign_keys='Absence.user_id', backref='employe', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def est_manager(self):
        return self.role == 'manager'

    @property
    def nom_complet(self):
        return f'{self.prenom} {self.nom}'

    def __repr__(self):
        return f'<User {self.email}>'


class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    date_service = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<Shift {self.employe.nom_complet} {self.date_service}>'


class Absence(db.Model):
    __tablename__ = 'absences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_absence = db.Column(db.String(30), nullable=False)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    motif = db.Column(db.Text, nullable=True)
    statut = db.Column(db.String(15), nullable=False, default='en_attente')
    commentaire_manager = db.Column(db.Text, nullable=True)
    traite_par = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Absence {self.employe.nom_complet} {self.date_debut}>'

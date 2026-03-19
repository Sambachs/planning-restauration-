import os

class Config:
    # Clé secrète pour sécuriser les sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cle-secrete-planning-resto'
    
    # Chemin vers la base de données SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///planning.db'
    
    # Désactive les notifications de modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
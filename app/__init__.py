from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'warning'

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.employees import bp as employees_bp
    app.register_blueprint(employees_bp)

    from app.shifts import bp as shifts_bp
    app.register_blueprint(shifts_bp)

    from app.absences import bp as absences_bp
    app.register_blueprint(absences_bp)

    from app.planning import bp as planning_bp
    app.register_blueprint(planning_bp)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

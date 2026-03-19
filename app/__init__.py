from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

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

    return app
    
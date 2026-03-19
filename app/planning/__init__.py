from flask import Blueprint

bp = Blueprint('planning', __name__)

from app.planning import routes
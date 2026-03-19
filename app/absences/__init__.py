from flask import Blueprint

bp = Blueprint('absences', __name__)

from app.absences import routes

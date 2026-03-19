from flask import Blueprint

bp = Blueprint('shifts', __name__)

from app.shifts import routes
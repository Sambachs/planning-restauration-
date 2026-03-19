from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.planning import bp
from app.models import Shift, Absence, User, Post
from datetime import date, timedelta

@bp.route('/')
@bp.route('/planning')
@login_required
def index():
    # Semaine actuelle
    aujourd_hui = date.today()
    debut_semaine = aujourd_hui - timedelta(days=aujourd_hui.weekday())
    fin_semaine = debut_semaine + timedelta(days=6)

    # Si manager → voit tous les créneaux
    # Si employé → voit seulement les siens
    if current_user.role == 'manager':
        shifts = Shift.query.filter(
            Shift.date >= debut_semaine,
            Shift.date <= fin_semaine
        ).all()
    else:
        shifts = Shift.query.filter(
            Shift.date >= debut_semaine,
            Shift.date <= fin_semaine,
            Shift.user_id == current_user.id
        ).all()

    return render_template('planning/index.html',
                           shifts=shifts,
                           debut_semaine=debut_semaine,
                           fin_semaine=fin_semaine,
                           aujourd_hui=aujourd_hui)
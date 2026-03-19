from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.absences import bp
from app.models import Absence, User
from datetime import datetime

def manager_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'manager':
            flash('Accès refusé.', 'danger')
            return redirect(url_for('planning.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/absences')
@login_required
def index():
    if current_user.role == 'manager':
        absences = Absence.query.order_by(Absence.date_demande.desc()).all()
    else:
        absences = Absence.query.filter_by(
            user_id=current_user.id
        ).order_by(Absence.date_demande.desc()).all()
    return render_template('absences/index.html', absences=absences)

@bp.route('/absences/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        date_debut = datetime.strptime(request.form.get('date_debut'), '%Y-%m-%d').date()
        date_fin = datetime.strptime(request.form.get('date_fin'), '%Y-%m-%d').date()
        motif = request.form.get('motif')
        type_absence = request.form.get('type_absence')

        absence = Absence(
            user_id=current_user.id,
            date_debut=date_debut,
            date_fin=date_fin,
            motif=motif,
            type_absence=type_absence,
            statut='en_attente'
        )
        db.session.add(absence)
        db.session.commit()
        flash('Demande envoyée avec succès !', 'success')
        return redirect(url_for('absences.index'))

    return render_template('absences/add.html')

@bp.route('/absences/approve/<int:id>')
@login_required
@manager_required
def approve(id):
    absence = Absence.query.get_or_404(id)
    absence.statut = 'approuvee'
    db.session.commit()
    flash('Demande approuvée !', 'success')
    return redirect(url_for('absences.index'))

@bp.route('/absences/refuse/<int:id>')
@login_required
@manager_required
def refuse(id):
    absence = Absence.query.get_or_404(id)
    absence.statut = 'refusee'
    db.session.commit()
    flash('Demande refusée.', 'warning')
    return redirect(url_for('absences.index'))

@bp.route('/absences/delete/<int:id>')
@login_required
def delete(id):
    absence = Absence.query.get_or_404(id)
    if absence.user_id != current_user.id and current_user.role != 'manager':
        flash('Accès refusé.', 'danger')
        return redirect(url_for('absences.index'))
    if absence.statut != 'en_attente':
        flash('Impossible de supprimer une demande déjà traitée.', 'danger')
        return redirect(url_for('absences.index'))
    db.session.delete(absence)
    db.session.commit()
    flash('Demande annulée avec succès !', 'success')
    return redirect(url_for('absences.index'))
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.shifts import bp
from app.models import Shift, User, Post
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

def check_conflict(user_id, date, heure_debut, heure_fin, shift_id=None):
    """Vérifie si un créneau est en conflit avec un autre"""
    query = Shift.query.filter(
        Shift.user_id == user_id,
        Shift.date == date,
        Shift.heure_debut < heure_fin,
        Shift.heure_fin > heure_debut
    )
    if shift_id:
        query = query.filter(Shift.id != shift_id)
    return query.first() is not None

@bp.route('/shifts')
@login_required
@manager_required
def index():
    shifts = Shift.query.order_by(Shift.date.desc()).all()
    return render_template('shifts/index.html', shifts=shifts)

@bp.route('/shifts/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add():
    employes = User.query.filter_by(est_actif=True).all()
    postes = Post.query.all()

    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        post_id = int(request.form.get('post_id'))
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        heure_debut = datetime.strptime(request.form.get('heure_debut'), '%H:%M').time()
        heure_fin = datetime.strptime(request.form.get('heure_fin'), '%H:%M').time()

        if check_conflict(user_id, date, heure_debut, heure_fin):
            flash('Conflit détecté : cet employé a déjà un créneau sur cette plage horaire.', 'danger')
            return redirect(url_for('shifts.add'))

        shift = Shift(
            user_id=user_id,
            post_id=post_id,
            date=date,
            heure_debut=heure_debut,
            heure_fin=heure_fin
        )
        db.session.add(shift)
        db.session.commit()
        flash('Créneau ajouté avec succès !', 'success')
        return redirect(url_for('shifts.index'))

    return render_template('shifts/add.html', employes=employes, postes=postes)

@bp.route('/shifts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@manager_required
def edit(id):
    shift = Shift.query.get_or_404(id)
    employes = User.query.filter_by(est_actif=True).all()
    postes = Post.query.all()

    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        post_id = int(request.form.get('post_id'))
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        heure_debut = datetime.strptime(request.form.get('heure_debut'), '%H:%M').time()
        heure_fin = datetime.strptime(request.form.get('heure_fin'), '%H:%M').time()

        if check_conflict(user_id, date, heure_debut, heure_fin, shift_id=id):
            flash('Conflit détecté : cet employé a déjà un créneau sur cette plage horaire.', 'danger')
            return redirect(url_for('shifts.edit', id=id))

        shift.user_id = user_id
        shift.post_id = post_id
        shift.date = date
        shift.heure_debut = heure_debut
        shift.heure_fin = heure_fin
        db.session.commit()
        flash('Créneau modifié avec succès !', 'success')
        return redirect(url_for('shifts.index'))

    return render_template('shifts/edit.html', shift=shift, employes=employes, postes=postes)

@bp.route('/shifts/delete/<int:id>')
@login_required
@manager_required
def delete(id):
    shift = Shift.query.get_or_404(id)
    db.session.delete(shift)
    db.session.commit()
    flash('Créneau supprimé avec succès !', 'success')
    return redirect(url_for('shifts.index'))
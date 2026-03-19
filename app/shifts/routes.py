from datetime import timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.shifts import bp
from app.shifts.forms import ShiftForm, DuplicateShiftForm
from app.auth.routes import manager_required
from app.models import Shift, User, Post


def check_conflict(user_id, date_service, heure_debut, heure_fin, exclude_id=None):
    query = Shift.query.filter(
        Shift.user_id == user_id,
        Shift.date_service == date_service,
        Shift.heure_debut < heure_fin,
        Shift.heure_fin > heure_debut,
    )
    if exclude_id:
        query = query.filter(Shift.id != exclude_id)
    return query.first()


def get_choices():
    employes = User.query.filter_by(role='employe', actif=True).order_by(User.nom).all()
    postes = Post.query.all()
    return employes, postes


@bp.route('/shifts/new', methods=['GET', 'POST'])
@login_required
@manager_required
def create_shift():
    employes, postes = get_choices()
    form = ShiftForm()
    form.set_choices(employes, postes)

    # Préremplissage depuis l'URL (ex: depuis le planning)
    if request.method == 'GET':
        date_param = request.args.get('date')
        user_param = request.args.get('employe', type=int)
        if date_param:
            from datetime import date
            try:
                form.date_service.data = date.fromisoformat(date_param)
            except ValueError:
                pass
        if user_param:
            form.user_id.data = user_param

    if form.validate_on_submit():
        conflit = check_conflict(
            form.user_id.data,
            form.date_service.data,
            form.heure_debut.data,
            form.heure_fin.data,
        )
        if conflit:
            employe = User.query.get(form.user_id.data)
            flash(
                f'Conflit : {employe.nom_complet} a déjà un créneau de '
                f'{conflit.heure_debut.strftime("%H:%M")} à {conflit.heure_fin.strftime("%H:%M")} ce jour-là.',
                'danger'
            )
            return render_template('shifts/form.html', form=form, titre='Nouveau créneau')

        shift = Shift(
            user_id=form.user_id.data,
            post_id=form.post_id.data,
            date_service=form.date_service.data,
            heure_debut=form.heure_debut.data,
            heure_fin=form.heure_fin.data,
            note=form.note.data or None,
            created_by=current_user.id,
        )
        db.session.add(shift)
        db.session.commit()
        flash('Créneau créé avec succès.', 'success')
        return redirect(url_for('planning.week_view', date=shift.date_service.isoformat()))

    return render_template('shifts/form.html', form=form, titre='Nouveau créneau')


@bp.route('/shifts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@manager_required
def edit_shift(id):
    shift = Shift.query.get_or_404(id)
    employes, postes = get_choices()
    form = ShiftForm(obj=shift)
    form.set_choices(employes, postes)

    if form.validate_on_submit():
        conflit = check_conflict(
            form.user_id.data,
            form.date_service.data,
            form.heure_debut.data,
            form.heure_fin.data,
            exclude_id=id,
        )
        if conflit:
            employe = User.query.get(form.user_id.data)
            flash(
                f'Conflit : {employe.nom_complet} a déjà un créneau de '
                f'{conflit.heure_debut.strftime("%H:%M")} à {conflit.heure_fin.strftime("%H:%M")} ce jour-là.',
                'danger'
            )
            return render_template('shifts/form.html', form=form, titre='Modifier le créneau', shift=shift)

        shift.user_id = form.user_id.data
        shift.post_id = form.post_id.data
        shift.date_service = form.date_service.data
        shift.heure_debut = form.heure_debut.data
        shift.heure_fin = form.heure_fin.data
        shift.note = form.note.data or None
        db.session.commit()
        flash('Créneau mis à jour.', 'success')
        return redirect(url_for('planning.week_view', date=shift.date_service.isoformat()))

    return render_template('shifts/form.html', form=form, titre='Modifier le créneau', shift=shift)


@bp.route('/shifts/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@manager_required
def delete_shift(id):
    shift = Shift.query.get_or_404(id)
    if request.method == 'POST':
        date_service = shift.date_service
        db.session.delete(shift)
        db.session.commit()
        flash('Créneau supprimé.', 'success')
        return redirect(url_for('planning.week_view', date=date_service.isoformat()))
    return render_template('shifts/confirm_delete.html', shift=shift)


@bp.route('/shifts/check-conflict', methods=['POST'])
@login_required
@manager_required
def check_conflict_ajax():
    data = request.get_json()
    try:
        from datetime import date, time
        user_id = int(data['user_id'])
        date_service = date.fromisoformat(data['date_service'])
        heure_debut = time.fromisoformat(data['heure_debut'])
        heure_fin = time.fromisoformat(data['heure_fin'])
        exclude_id = data.get('exclude_id')

        conflit = check_conflict(user_id, date_service, heure_debut, heure_fin, exclude_id)
        if conflit:
            return jsonify({
                'conflict': True,
                'message': f'Créneau existant : {conflit.heure_debut.strftime("%H:%M")} – {conflit.heure_fin.strftime("%H:%M")}'
            })
        return jsonify({'conflict': False})
    except Exception:
        return jsonify({'conflict': False})


@bp.route('/shifts/<int:id>/duplicate', methods=['GET', 'POST'])
@login_required
@manager_required
def duplicate_shift(id):
    shift = Shift.query.get_or_404(id)
    form = DuplicateShiftForm()

    if form.validate_on_submit():
        date_courante = form.date_debut.data
        crees, ignores = 0, 0

        while date_courante <= form.date_fin.data:
            if date_courante != shift.date_service:
                if not check_conflict(shift.user_id, date_courante, shift.heure_debut, shift.heure_fin):
                    db.session.add(Shift(
                        user_id=shift.user_id,
                        post_id=shift.post_id,
                        date_service=date_courante,
                        heure_debut=shift.heure_debut,
                        heure_fin=shift.heure_fin,
                        note=shift.note,
                        created_by=current_user.id,
                    ))
                    crees += 1
                else:
                    ignores += 1
            date_courante += timedelta(days=1)

        db.session.commit()
        msg = f'{crees} créneau(x) créé(s).'
        if ignores:
            msg += f' {ignores} ignoré(s) pour cause de conflit.'
        flash(msg, 'success')
        return redirect(url_for('planning.week_view', date=shift.date_service.isoformat()))

    return render_template('shifts/duplicate_form.html', form=form, shift=shift)

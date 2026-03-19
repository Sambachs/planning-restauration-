from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.absences import bp
from app.absences.forms import AbsenceRequestForm, ManualAbsenceForm, RejectAbsenceForm
from app.auth.routes import manager_required
from app.models import Absence, User


# ── Employé ──────────────────────────────────────────────────────────────────

@bp.route('/absences/my')
@login_required
def my_absences():
    absences = Absence.query.filter_by(user_id=current_user.id)\
                            .order_by(Absence.created_at.desc()).all()
    return render_template('absences/my_absences.html', absences=absences)


@bp.route('/absences/request', methods=['GET', 'POST'])
@login_required
def request_absence():
    form = AbsenceRequestForm()
    if form.validate_on_submit():
        absence = Absence(
            user_id=current_user.id,
            type_absence=form.type_absence.data,
            date_debut=form.date_debut.data,
            date_fin=form.date_fin.data,
            motif=form.motif.data or None,
            statut='en_attente',
        )
        db.session.add(absence)
        db.session.commit()
        flash('Votre demande de congé a été soumise.', 'success')
        return redirect(url_for('absences.my_absences'))
    return render_template('absences/request_form.html', form=form)


@bp.route('/absences/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_absence(id):
    absence = Absence.query.get_or_404(id)
    if absence.user_id != current_user.id:
        abort(403)
    if absence.statut != 'en_attente':
        flash('Seules les demandes en attente peuvent être annulées.', 'danger')
        return redirect(url_for('absences.my_absences'))
    db.session.delete(absence)
    db.session.commit()
    flash('Demande annulée.', 'success')
    return redirect(url_for('absences.my_absences'))


# ── Manager ───────────────────────────────────────────────────────────────────

@bp.route('/absences/')
@login_required
@manager_required
def list_absences():
    filtre_statut = request.args.get('statut', 'tous')
    filtre_employe = request.args.get('employe', type=int)

    query = Absence.query
    if filtre_statut != 'tous':
        query = query.filter_by(statut=filtre_statut)
    if filtre_employe:
        query = query.filter_by(user_id=filtre_employe)

    absences = query.order_by(Absence.created_at.desc()).all()
    employes = User.query.filter_by(role='employe', actif=True).order_by(User.nom).all()
    nb_attente = Absence.query.filter_by(statut='en_attente').count()

    return render_template('absences/list.html', absences=absences,
                           employes=employes, filtre_statut=filtre_statut,
                           filtre_employe=filtre_employe, nb_attente=nb_attente)


@bp.route('/absences/<int:id>/approve', methods=['POST'])
@login_required
@manager_required
def approve_absence(id):
    absence = Absence.query.get_or_404(id)
    if absence.statut != 'en_attente':
        flash('Cette demande a déjà été traitée.', 'warning')
        return redirect(url_for('absences.list_absences'))
    absence.statut = 'approuve'
    absence.traite_par = current_user.id
    db.session.commit()
    flash(f'Demande de {absence.employe.nom_complet} approuvée.', 'success')
    return redirect(request.referrer or url_for('absences.list_absences'))


@bp.route('/absences/<int:id>/reject', methods=['GET', 'POST'])
@login_required
@manager_required
def reject_absence(id):
    absence = Absence.query.get_or_404(id)
    if absence.statut != 'en_attente':
        flash('Cette demande a déjà été traitée.', 'warning')
        return redirect(url_for('absences.list_absences'))
    form = RejectAbsenceForm()
    if form.validate_on_submit():
        absence.statut = 'refuse'
        absence.traite_par = current_user.id
        absence.commentaire_manager = form.commentaire_manager.data or None
        db.session.commit()
        flash(f'Demande de {absence.employe.nom_complet} refusée.', 'success')
        return redirect(url_for('absences.list_absences'))
    return render_template('absences/reject_form.html', form=form, absence=absence)


@bp.route('/absences/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add_absence():
    employes = User.query.filter_by(role='employe', actif=True).order_by(User.nom).all()
    form = ManualAbsenceForm()
    form.set_employe_choices(employes)
    if form.validate_on_submit():
        absence = Absence(
            user_id=form.user_id.data,
            type_absence=form.type_absence.data,
            date_debut=form.date_debut.data,
            date_fin=form.date_fin.data,
            motif=form.motif.data or None,
            statut='confirme',
            traite_par=current_user.id,
        )
        db.session.add(absence)
        db.session.commit()
        employe = User.query.get(form.user_id.data)
        flash(f'Absence de {employe.nom_complet} enregistrée.', 'success')
        return redirect(url_for('absences.list_absences'))
    return render_template('absences/add_form.html', form=form)

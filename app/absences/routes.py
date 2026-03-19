from flask import render_template, request
from flask_login import login_required, current_user
from app.absences import bp
from app.auth.routes import manager_required
from app.models import Absence, User


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


@bp.route('/absences/my')
@login_required
def my_absences():
    absences = Absence.query.filter_by(user_id=current_user.id)\
                            .order_by(Absence.created_at.desc()).all()
    return render_template('absences/my_absences.html', absences=absences)


@bp.route('/absences/request', methods=['GET', 'POST'])
@login_required
def request_absence():
    return render_template('absences/request_form.html')


@bp.route('/absences/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_absence(id):
    return '', 204


@bp.route('/absences/<int:id>/approve', methods=['POST'])
@login_required
@manager_required
def approve_absence(id):
    return '', 204


@bp.route('/absences/<int:id>/reject', methods=['POST'])
@login_required
@manager_required
def reject_absence(id):
    return '', 204


@bp.route('/absences/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add_absence():
    return render_template('absences/add_form.html')

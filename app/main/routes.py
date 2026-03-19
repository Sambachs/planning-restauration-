from datetime import date, timedelta
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Shift, Absence


def get_semaine_courante():
    today = date.today()
    lundi = today - timedelta(days=today.weekday())
    dimanche = lundi + timedelta(days=6)
    return lundi, dimanche


@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.est_manager:
        return _dashboard_manager()
    return _dashboard_employe()


def _dashboard_manager():
    lundi, dimanche = get_semaine_courante()
    today = date.today()

    nb_employes = User.query.filter_by(role='employe', actif=True).count()
    nb_creneaux_semaine = Shift.query.filter(
        Shift.date_service >= lundi,
        Shift.date_service <= dimanche
    ).count()
    nb_attente = Absence.query.filter_by(statut='en_attente').count()

    prochains_creneaux = Shift.query.filter(
        Shift.date_service >= today
    ).order_by(Shift.date_service, Shift.heure_debut).limit(8).all()

    demandes_attente = Absence.query.filter_by(statut='en_attente')\
                                    .order_by(Absence.created_at).all()

    return render_template('dashboard_manager.html',
        nb_employes=nb_employes,
        nb_creneaux_semaine=nb_creneaux_semaine,
        nb_attente=nb_attente,
        prochains_creneaux=prochains_creneaux,
        demandes_attente=demandes_attente,
        today=today,
    )


def _dashboard_employe():
    lundi, dimanche = get_semaine_courante()
    today = date.today()

    creneaux_semaine = Shift.query.filter(
        Shift.user_id == current_user.id,
        Shift.date_service >= lundi,
        Shift.date_service <= dimanche,
    ).order_by(Shift.date_service, Shift.heure_debut).all()

    dernieres_demandes = Absence.query.filter_by(user_id=current_user.id)\
                                      .order_by(Absence.created_at.desc()).limit(3).all()

    prochain_shift = Shift.query.filter(
        Shift.user_id == current_user.id,
        Shift.date_service >= today,
    ).order_by(Shift.date_service, Shift.heure_debut).first()

    JOURS_FR = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    return render_template('dashboard_employee.html',
        creneaux_semaine=creneaux_semaine,
        dernieres_demandes=dernieres_demandes,
        prochain_shift=prochain_shift,
        jours_fr=JOURS_FR,
        today=today,
    )

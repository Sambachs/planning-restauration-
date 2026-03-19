from datetime import date, timedelta
from flask import render_template, request
from flask_login import login_required, current_user
from app.planning import bp
from app.models import Shift, Absence, User, Post


def get_semaine(date_ref):
    lundi = date_ref - timedelta(days=date_ref.weekday())
    return [lundi + timedelta(days=i) for i in range(7)]


@bp.route('/planning/week')
@login_required
def week_view():
    date_param = request.args.get('date')
    if date_param:
        try:
            date_ref = date.fromisoformat(date_param)
        except ValueError:
            date_ref = date.today()
    else:
        date_ref = date.today()

    semaine = get_semaine(date_ref)
    lundi, dimanche = semaine[0], semaine[6]

    filtre_employe = request.args.get('employe', type=int)
    filtre_poste = request.args.get('poste', type=int)

    query = Shift.query.filter(Shift.date_service >= lundi, Shift.date_service <= dimanche)
    if not current_user.est_manager:
        query = query.filter(Shift.user_id == current_user.id)
    elif filtre_employe:
        query = query.filter(Shift.user_id == filtre_employe)
    elif filtre_poste:
        query = query.filter(Shift.post_id == filtre_poste)

    shifts = query.order_by(Shift.heure_debut).all()

    creneaux_par_jour = {jour: [] for jour in semaine}
    for shift in shifts:
        if shift.date_service in creneaux_par_jour:
            creneaux_par_jour[shift.date_service].append(shift)

    absences = Absence.query.filter(
        Absence.statut.in_(['approuve', 'confirme']),
        Absence.date_debut <= dimanche,
        Absence.date_fin >= lundi,
    ).all()

    employes = User.query.filter_by(role='employe', actif=True).order_by(User.nom).all() if current_user.est_manager else []
    postes = Post.query.all() if current_user.est_manager else []

    prev_week = (lundi - timedelta(7)).isoformat()
    next_week = (lundi + timedelta(7)).isoformat()

    JOURS_FR = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    return render_template('planning/week.html',
        semaine=semaine,
        jours_fr=JOURS_FR,
        creneaux_par_jour=creneaux_par_jour,
        absences=absences,
        employes=employes,
        postes=postes,
        prev_week=prev_week,
        next_week=next_week,
        filtre_employe=filtre_employe,
        filtre_poste=filtre_poste,
        today=date.today(),
    )


@bp.route('/planning/month')
@login_required
def month_view():
    import calendar

    date_param = request.args.get('date')
    if date_param:
        try:
            date_ref = date.fromisoformat(date_param)
        except ValueError:
            date_ref = date.today()
    else:
        date_ref = date.today()

    annee, mois = date_ref.year, date_ref.month
    premier_jour = date(annee, mois, 1)
    dernier_jour = date(annee, mois, calendar.monthrange(annee, mois)[1])

    filtre_employe = request.args.get('employe', type=int)

    query = Shift.query.filter(Shift.date_service >= premier_jour, Shift.date_service <= dernier_jour)
    if not current_user.est_manager:
        query = query.filter(Shift.user_id == current_user.id)
    elif filtre_employe:
        query = query.filter(Shift.user_id == filtre_employe)

    shifts = query.order_by(Shift.heure_debut).all()
    creneaux_par_jour = {}
    for shift in shifts:
        creneaux_par_jour.setdefault(shift.date_service, []).append(shift)

    absences = Absence.query.filter(
        Absence.statut.in_(['approuve', 'confirme']),
        Absence.date_debut <= dernier_jour,
        Absence.date_fin >= premier_jour,
    ).all()

    # Construire la grille calendrier (semaines)
    cal = calendar.monthcalendar(annee, mois)
    employes = User.query.filter_by(role='employe', actif=True).order_by(User.nom).all() if current_user.est_manager else []

    mois_prev = date(annee - 1 if mois == 1 else annee, 12 if mois == 1 else mois - 1, 1)
    mois_next = date(annee + 1 if mois == 12 else annee, 1 if mois == 12 else mois + 1, 1)

    MOIS_FR = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
               'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    JOURS_FR = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

    return render_template('planning/month.html',
        cal=cal,
        annee=annee,
        mois=mois,
        mois_nom=MOIS_FR[mois],
        jours_fr=JOURS_FR,
        creneaux_par_jour=creneaux_par_jour,
        absences=absences,
        employes=employes,
        filtre_employe=filtre_employe,
        mois_prev=mois_prev.isoformat(),
        mois_next=mois_next.isoformat(),
        today=date.today(),
    )

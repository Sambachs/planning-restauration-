from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.employees import bp
from app.employees.forms import EmployeeForm
from app.auth.routes import manager_required
from app.models import User, Post, Shift


@bp.route('/employees/')
@login_required
@manager_required
def list_employees():
    filtre_poste = request.args.get('poste', type=int)
    filtre_statut = request.args.get('statut', 'actif')

    query = User.query.filter_by(role='employe')
    if filtre_statut == 'actif':
        query = query.filter_by(actif=True)
    elif filtre_statut == 'inactif':
        query = query.filter_by(actif=False)
    if filtre_poste:
        query = query.filter_by(post_id=filtre_poste)

    employes = query.order_by(User.nom).all()
    postes = Post.query.all()
    return render_template('employees/list.html', employes=employes, postes=postes,
                           filtre_poste=filtre_poste, filtre_statut=filtre_statut)


@bp.route('/employees/new', methods=['GET', 'POST'])
@login_required
@manager_required
def create_employee():
    postes = Post.query.all()
    form = EmployeeForm()
    form.set_post_choices(postes)

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash('Un compte avec cet email existe déjà.', 'danger')
            return render_template('employees/form.html', form=form, titre='Nouvel employé')

        if not form.password.data:
            flash('Le mot de passe est obligatoire à la création.', 'danger')
            return render_template('employees/form.html', form=form, titre='Nouvel employé')

        employe = User(
            nom=form.nom.data.strip(),
            prenom=form.prenom.data.strip(),
            email=form.email.data.lower().strip(),
            telephone=form.telephone.data or None,
            post_id=form.post_id.data if form.post_id.data != 0 else None,
            contrat=form.contrat.data,
            date_embauche=form.date_embauche.data,
            role=form.role.data,
        )
        employe.set_password(form.password.data)
        db.session.add(employe)
        db.session.commit()
        flash(f'Employé {employe.nom_complet} créé avec succès.', 'success')
        return redirect(url_for('employees.list_employees'))

    return render_template('employees/form.html', form=form, titre='Nouvel employé')


@bp.route('/employees/<int:id>')
@login_required
@manager_required
def view_employee(id):
    employe = User.query.get_or_404(id)
    from datetime import date
    prochains_shifts = Shift.query.filter(
        Shift.user_id == id,
        Shift.date_service >= date.today()
    ).order_by(Shift.date_service, Shift.heure_debut).limit(5).all()
    return render_template('employees/detail.html', employe=employe, prochains_shifts=prochains_shifts)


@bp.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@manager_required
def edit_employee(id):
    employe = User.query.get_or_404(id)
    postes = Post.query.all()
    form = EmployeeForm(obj=employe)
    form.set_post_choices(postes)

    if form.validate_on_submit():
        email_existant = User.query.filter_by(email=form.email.data.lower()).first()
        if email_existant and email_existant.id != id:
            flash('Cet email est déjà utilisé par un autre compte.', 'danger')
            return render_template('employees/form.html', form=form, titre='Modifier l\'employé', employe=employe)

        employe.nom = form.nom.data.strip()
        employe.prenom = form.prenom.data.strip()
        employe.email = form.email.data.lower().strip()
        employe.telephone = form.telephone.data or None
        employe.post_id = form.post_id.data if form.post_id.data != 0 else None
        employe.contrat = form.contrat.data
        employe.date_embauche = form.date_embauche.data
        employe.role = form.role.data

        if form.password.data:
            employe.set_password(form.password.data)

        db.session.commit()
        flash(f'Employé {employe.nom_complet} mis à jour.', 'success')
        return redirect(url_for('employees.view_employee', id=id))

    return render_template('employees/form.html', form=form, titre='Modifier l\'employé', employe=employe)


@bp.route('/employees/<int:id>/toggle', methods=['POST'])
@login_required
@manager_required
def toggle_employee(id):
    employe = User.query.get_or_404(id)
    employe.actif = not employe.actif
    db.session.commit()
    statut = 'réactivé' if employe.actif else 'désactivé'
    flash(f'Compte de {employe.nom_complet} {statut}.', 'success')
    return redirect(url_for('employees.view_employee', id=id))

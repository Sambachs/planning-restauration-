from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.employees import bp
from app.models import User
import bcrypt

# Vérification que l'utilisateur est manager
def manager_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'manager':
            flash('Accès refusé.', 'danger')
            return redirect(url_for('planning.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/employees')
@login_required
@manager_required
def index():
    employes = User.query.filter_by(est_actif=True).all()
    return render_template('employees/index.html', employes=employes)

@bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        type_contrat = request.form.get('type_contrat')
        role = request.form.get('role')

        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('employees.add'))

        mot_de_passe = bcrypt.hashpw(
            'password123'.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        employe = User(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            type_contrat=type_contrat,
            role=role,
            mot_de_passe=mot_de_passe,
            est_actif=True
        )
        db.session.add(employe)
        db.session.commit()
        flash(f'Employé {prenom} {nom} ajouté avec succès !', 'success')
        return redirect(url_for('employees.index'))

    return render_template('employees/add.html')

@bp.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@manager_required
def edit(id):
    employe = User.query.get_or_404(id)

    if request.method == 'POST':
        employe.nom = request.form.get('nom')
        employe.prenom = request.form.get('prenom')
        employe.email = request.form.get('email')
        employe.telephone = request.form.get('telephone')
        employe.type_contrat = request.form.get('type_contrat')
        employe.role = request.form.get('role')
        db.session.commit()
        flash('Employé modifié avec succès !', 'success')
        return redirect(url_for('employees.index'))

    return render_template('employees/edit.html', employe=employe)

@bp.route('/employees/delete/<int:id>')
@login_required
@manager_required
def delete(id):
    employe = User.query.get_or_404(id)
    employe.est_actif = False
    db.session.commit()
    flash('Employé désactivé avec succès !', 'success')
    return redirect(url_for('employees.index'))
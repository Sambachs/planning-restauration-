from flask import render_template, request
from flask_login import login_required
from app.employees import bp
from app.auth.routes import manager_required
from app.models import User, Post


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
    return render_template('employees/form.html')


@bp.route('/employees/<int:id>')
@login_required
@manager_required
def view_employee(id):
    employe = User.query.get_or_404(id)
    return render_template('employees/detail.html', employe=employe)


@bp.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@manager_required
def edit_employee(id):
    employe = User.query.get_or_404(id)
    return render_template('employees/form.html', employe=employe)


@bp.route('/employees/<int:id>/toggle', methods=['POST'])
@login_required
@manager_required
def toggle_employee(id):
    return '', 204

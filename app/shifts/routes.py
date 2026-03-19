from flask import render_template
from flask_login import login_required
from app.shifts import bp
from app.auth.routes import manager_required


@bp.route('/shifts/new', methods=['GET', 'POST'])
@login_required
@manager_required
def create_shift():
    return render_template('shifts/form.html')


@bp.route('/shifts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@manager_required
def edit_shift(id):
    return render_template('shifts/form.html')


@bp.route('/shifts/<int:id>/delete', methods=['POST'])
@login_required
@manager_required
def delete_shift(id):
    return '', 204


@bp.route('/shifts/check-conflict', methods=['POST'])
@login_required
@manager_required
def check_conflict():
    return {'conflict': False}


@bp.route('/shifts/<int:id>/duplicate', methods=['POST'])
@login_required
@manager_required
def duplicate_shift(id):
    return '', 204

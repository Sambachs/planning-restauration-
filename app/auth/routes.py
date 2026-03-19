from functools import wraps
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user

from app.auth import bp
from app.auth.forms import LoginForm
from app.models import User


def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.est_manager:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('planning.week_view'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash('Email ou mot de passe incorrect.', 'danger')
            return render_template('auth/login.html', form=form)

        if not user.actif:
            flash('Ce compte est désactivé. Contactez votre manager.', 'danger')
            return render_template('auth/login.html', form=form)

        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('planning.week_view'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))

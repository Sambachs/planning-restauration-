from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.auth import bp
from app.models import User
import bcrypt

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('planning.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(mot_de_passe.encode('utf-8'), user.mot_de_passe.encode('utf-8')):
            if user.est_actif:
                login_user(user)
                return redirect(url_for('planning.index'))
            else:
                flash('Votre compte est désactivé.', 'danger')
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

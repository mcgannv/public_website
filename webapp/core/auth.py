from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash

from .models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.controls'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(
            username=username,
        ).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('main.controls'))

    return render_template('main/login.html')


@auth.route('/logout')
def logout():
    return 'Logout'

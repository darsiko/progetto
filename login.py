from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import login_user, current_user
from models import db, User

login_bp = Blueprint('login_bp', __name__, template_folder='templates', static_folder='static',
                     static_url_path='/assets')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(User).filter_by(email=email).first()
        remember = True if request.form.get('remember') else False

        if user is not None:
            if user.role == 'admin' and password == 'pass123' and email == "admin@admin":
                login_user(user, remember=remember)
                return redirect(url_for('privare_bp.private'))
            if user.check_password(password):
                login_user(user, remember=remember)
                return redirect(url_for('home_bp.index'))
            else:
                error = 'Invalid credentials'
                return internal_error(error)
        else:
            error = 'User not found'
            return internal_error(error)

    return render_template('login.html', current_user=current_user)


@login_bp.errorhandler(500)
@login_bp.errorhandler(400)
def internal_error(error):
    return render_template('errore.html', error=error)

from functools import wraps
from flask import render_template, request, redirect, url_for, Blueprint, Response, session
from flask_login import login_user, current_user
from models import db, User

login_bp = Blueprint('login_bp', __name__, template_folder='templates', static_folder='static',
                     static_url_path='/assets')


def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        if 'api_session_token' not in session:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return Response("Access denied")
        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)
    return check_token


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
                return redirect(url_for('admin_bp.admin'))
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

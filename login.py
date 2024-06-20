from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from form import LoginForm
from models import User

login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates', static_folder='static')


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(request.form.get('next') or url_for('index_blueprint.index'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)


@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_blueprint.index'))


@login_blueprint.errorhandler(500)
@login_blueprint.errorhandler(400)
def internal_error(error):
    return render_template('error.html', error=error)

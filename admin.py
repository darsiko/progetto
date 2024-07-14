from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_user
from sqlalchemy.testing.pickleable import User

from form import LoginForm
from models import User

admin_blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin_blueprint.route("/admin", methods=['GET', 'POST'])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.role == 'admin' and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(request.form.get('next') or url_for('index_blueprint.index'))
        else:
            flash("Invalid credentials")

    return render_template("admin.html", form=form)

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from werkzeug.exceptions import Unauthorized
from models import User, db
from form import ModifyUser

users_blueprint = Blueprint('users_blueprint', __name__, template_folder='templates', static_folder='static')


@users_blueprint.route('/users')
def users():
    if current_user.role == 'admin':
        user = User.query.all()
        return render_template("users.html", users=user)
    else:
        raise Unauthorized()


@users_blueprint.route('/<int:idx>/users/modify', methods=['GET', 'POST'])
def modify(idx):
    if current_user.role == 'admin':
        user = User.query.filter_by(id=idx).first()
        form = ModifyUser(obj=user)
        if form.validate_on_submit():
            user.name = form.name.data
            user.email = form.email.data
            user.address = form.address.data
            user.role = form.role.data
            db.session.commit()
            return redirect(url_for('users_blueprint.users'))
        return render_template('modify_users.html', form=form)
    else:
        raise Unauthorized()


@users_blueprint.route('/<int:idx>/delete', methods=['POST'])
def delete(idx):
    if current_user.role == 'admin':
        user = User.query.get_or_404(idx)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users_blueprint.users'))
    else:
        raise Unauthorized()


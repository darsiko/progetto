from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from werkzeug.exceptions import Unauthorized
from models import User, db

users_blueprint = Blueprint('users_blueprint', __name__, template_folder='templates', static_folder='static')


@users_blueprint.route('/users')
def users():
    if current_user.role == 'admin':
        users = User.query.all()
        return render_template("users.html", users=users)
    else:
        raise Unauthorized()


@users_blueprint.route('/users/modify', methods=['GET', 'POST'])
def modify():
    if current_user.role == 'admin':
        return render_template('modify_users.html')
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


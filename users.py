from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.exceptions import Unauthorized
from models import User

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


@users_blueprint.route(methods=['GET', 'POST'])
def delete(id):
    if current_user.role == 'admin':
        User.query.filter_by(id=id).delete()
        return None
    else:
        raise Unauthorized()
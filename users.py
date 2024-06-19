from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

users_blueprint = Blueprint('users_blueprint', __name__, template_folder='templates', static_folder='static')


@users_blueprint.route('/users')
def users():
    if current_user.role == 'admin':
        return render_template("users.html")
    else:
        raise Unauthorized()

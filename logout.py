from flask import render_template, Blueprint
from flask_login import login_required, logout_user

from models import session

logout_bp = Blueprint('logout_bp', __name__, template_folder='templates', static_folder='static')


@logout_bp.route('/')
@login_required
def logout():
    logout_user()
    session.close()
    return render_template('layout.html')

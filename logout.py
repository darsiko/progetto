from flask import render_template, Blueprint

logout_bp = Blueprint('logout_bp', __name__, template_folder='templates', static_folder='static')

@logout_bp.route('/')
def logout():
    return render_template('logout/index.html')
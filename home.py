from flask import render_template, Blueprint
from flask_login import current_user

home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@home_bp.route('/')
def index():
    if current_user:
        return render_template('index.html')
    return render_template('layout.html', current_user=current_user)

from flask import render_template, Blueprint

home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@home_bp.route('/')
def index():
    return render_template('index.html')

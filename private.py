from flask import render_template, Blueprint

private_bp = Blueprint('private_bp', __name__, template_folder='templates', static_folder='static')

@private_bp.route('/private')
def private():
    return render_template('private/private.html')
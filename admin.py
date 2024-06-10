from flask import render_template, Blueprint

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static',
                     static_url_path='/assets')


@admin_bp.route('/admin')
def admin():
    return render_template('admin.html')

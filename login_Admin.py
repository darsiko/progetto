from flask import render_template, request, redirect, Blueprint
from login import internal_error

login_admin_bp = Blueprint('login_admin_bp', __name__, template_folder='templates', static_folder='static',
                           static_url_path='/assets')


@login_admin_bp.route('/admin_login', methods=['GET', 'POST'])
def login_admin():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email == "admin@admin" and password == "pass123":
            return redirect('/admin')
        else:
            error = 'Invalid credentials'
            return internal_error(error)

    return render_template('admin_login.html')

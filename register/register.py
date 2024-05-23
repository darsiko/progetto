from flask import render_template, request, redirect, Blueprint
from models import db, User

register_bp = Blueprint('register_bp', __name__, template_folder='templates', static_folder='static',
                        static_url_path='/assets')


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email_register = request.form['email']
        password = request.form['password']
        address = request.form['address']
        role = request.form.get('select')
        users = User(name=name, email=email_register, password=password, role=role)
        users.set_password(password)
        db.session.add(users)
        db.session.commit()
        return redirect('/login')
    return render_template('register/register.html')

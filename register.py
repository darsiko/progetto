from flask import Blueprint, render_template, flash, redirect, url_for
from models import User, db
from form import RegisterForm

register_blueprint = Blueprint('register_blueprint', __name__, template_folder='templates', static_folder='static')


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data, password=form.password.data, address=form.address.data, role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login_blueprint.login'))
    return render_template('register.html', form=form)

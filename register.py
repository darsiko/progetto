from flask import Blueprint, render_template, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from models import User, db
from form import RegisterForm

register_blueprint = Blueprint('register_blueprint', __name__, template_folder='templates', static_folder='static')


@register_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            new_user = User(name=form.name.data, email=form.email.data, password=form.password.data,
                            address=form.address.data, role=form.role.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login_blueprint.login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = str(e.__cause__)
            if 'Username' in error_message:
                flash('Error: Username already exists. Please choose a different one.')
            elif 'Email' in error_message:
                flash('Error: Email already exists. Please choose a different one.')
            else:
                flash('An unexpected error occurred. Please try again.')
    return render_template('register.html', form=form)

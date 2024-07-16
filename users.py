from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.exceptions import Unauthorized
from models import User, db
from form import ModifyUser

users_blueprint = Blueprint('users_blueprint', __name__, template_folder='templates', static_folder='static')


@users_blueprint.route('/users')
def users():
    if current_user.role == 'admin':
        user = User.query.all()
        return render_template("users.html", users=user)
    else:
        return render_template("unauthorized.html"), 403


@users_blueprint.route('/users/modify/<int:idx>', methods=['GET', 'POST'])
def modify(idx):
    if current_user.role == 'admin':
        user = User.query.filter_by(id=idx).first()
        form = ModifyUser(obj=user)
        if form.validate_on_submit():
            user.name = form.name.data
            user.email = form.email.data
            user.address = form.address.data
            user.role = form.role.data
            db.session.commit()
            return redirect(url_for('users_blueprint.users'))
        return render_template('modify_users.html', form=form)
    else:
        return render_template("unauthorized.html"), 403


@users_blueprint.route('/users/delete/<int:idx>', methods=['POST'])
def delete(idx):
    if current_user.role == 'admin':
        user = User.query.get_or_404(idx)
        db.session.delete(user)
        db.session.commit()
        return redirect(request.headers.get('Referer'))
    else:
        return render_template("unauthorized.html"), 403


@users_blueprint.route('/private_area/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = User.query.filter_by(id=current_user.id).first()
    form = ModifyUser(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.address = form.address.data
        db.session.commit()
        return redirect(url_for('private_area_blueprint.private_area'))
    return render_template('modify_users.html', form=form)

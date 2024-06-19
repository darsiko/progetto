from flask import Blueprint, render_template

private_area_blueprint = Blueprint('private_area_blueprint', __name__, template_folder='templates', static_folder='static')


@private_area_blueprint.route('/private_area')
def private_area():
    return render_template('private_area.html')

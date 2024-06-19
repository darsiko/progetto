from flask import Blueprint, render_template
from flask_login import login_required

orders_blueprint = Blueprint('orders_blueprint', __name__, template_folder='templates', static_folder='static')


@orders_blueprint.route('/orders')
@login_required
def orders():
    return render_template('orders.html')



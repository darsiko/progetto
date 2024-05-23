from flask import render_template, Blueprint

cart_bp = Blueprint('cart_bp', __name__, template_folder='templates', static_folder='static')
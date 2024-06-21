from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from models import Product, db

products_blueprint = Blueprint('products_blueprint', __name__, template_folder="templates", static_folder="static")


@products_blueprint.route("/products")
def products():
    items = Product.query.all()
    return render_template("products.html", products=items)


@products_blueprint.route('/<int:idx>/delete', methods=['POST'])
def delete(idx):
    if current_user.role == 'admin':
        product = Product.query.get_or_404(idx)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('products_blueprint.products'))
    else:
        raise Unauthorized()


@products_blueprint.route('/<int:idx>/own_products', methods=['GET', 'POST'])
def own_products(idx):
    if current_user.role == 'seller':
        prod = Product.query.filter_by(seller_id=idx)
        return render_template('own_products.html', products=prod)
    else:
        raise Unauthorized()

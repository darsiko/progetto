from flask import Blueprint, render_template

from models import Product

products_blueprint = Blueprint('products_blueprint', __name__, template_folder="templates", static_folder="static")


@products_blueprint.route("/products")
def products():
    items = Product.query.all()
    return render_template("products.html", products=items)

from flask import Blueprint, render_template
from models import Product, Category

index_blueprint = Blueprint('index_blueprint', __name__, template_folder="templates", static_folder="static")


@index_blueprint.route("/")
def index():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template("index.html", products=products, categories=categories)

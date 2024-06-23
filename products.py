from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from werkzeug.exceptions import Unauthorized
from form import AddProductForm
from models import Product, db, Cart, CartItem

products_blueprint = Blueprint('products_blueprint', __name__, template_folder="templates", static_folder="static")


@products_blueprint.route("/products")
def products():
    items = Product.query.all()
    return render_template("products.html", products=items)


@products_blueprint.route('/<int:idx>/delete', methods=['POST'])
def delete(idx):
    if current_user.role == 'admin' or current_user.role == 'seller':
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


@products_blueprint.route('/own_products/add', methods=['GET', 'POST'])
def add_product():
    if current_user.role == 'seller':
        form = AddProductForm()
        if form.validate_on_submit():
            new_product = Product(name=form.name.data, seller_id=current_user.id, description=form.description.data, amount=form.amount.data, price=form.price.data)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for("products_blueprint.own_products", idx=current_user.id))
        return render_template("add_product.html", form=form)
    else:
        raise Unauthorized()


@products_blueprint.route('/<int:idx>/add_to_cart', methods=['POST'])
def add_to_cart(idx):
    return redirect(url_for('products_blueprint.products'))


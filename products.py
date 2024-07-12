import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import current_user
from sqlalchemy import func
from werkzeug.exceptions import Unauthorized
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload

from form import AddProductForm
from models import Product, db, Review, ProductCategory, Category

products_blueprint = Blueprint('products_blueprint', __name__, template_folder="templates", static_folder="static")


@products_blueprint.route("/products")
def products():
    items = Product.query.all()
    item_with_score = []
    for i in items:
        avg = db.session.query(func.avg(Review.score)).filter(Review.product_id == i.id).scalar()
        if avg is not None:
            avg = round(avg, 1)
        item_with_score.append({
            'id': i.id,
            'name': i.name,
            'price': i.price,
            'description': i.description,
            'amount': i.amount,
            'avg': avg
        })
    return render_template("products.html", products=item_with_score)


@products_blueprint.route('/<int:idx>/delete', methods=['POST'])
def delete(idx):
    if current_user.role == 'admin' or current_user.role == 'seller':
        product = Product.query.get_or_404(idx)
        db.session.delete(product)
        db.session.commit()
        return redirect(request.headers.get('Referer'))
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
    if current_user.role == 'seller' or current_user.role == 'admin':
        form = AddProductForm()
        if form.validate_on_submit():
            new_product = Product(name=form.name.data, seller_id=current_user.id, description=form.description.data,
                                  amount=form.amount.data, price=form.price.data)

            db.session.add(new_product)
            db.session.flush()

            category_name = form.category.data
            category = Category.query.filter_by(name=category_name).first()

            new_product_category = ProductCategory(product_id=new_product.id, category_id=category.id)
            db.session.add(new_product_category)

            product_id = new_product.id

            file = form.file.data
            if file:
                filename = f"{product_id}.jpg"
                file.save(os.path.join(current_app.config['UPLOADED_FOLDER'], filename))

            db.session.commit()

            return redirect(url_for("products_blueprint.own_products", idx=current_user.id))
        return render_template("add_product.html", form=form)
    else:
        raise Unauthorized()


@products_blueprint.route('/<int:idx>/own_products/modify', methods=['POST'])
def modify_product(idx):
    if current_user.role == 'seller' or current_user.role == 'admin':
        product = Product.query.filter_by(id=idx).first()
        form = AddProductForm(obj=product)
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.amount = form.amount.data
            product.price = form.price.data

            if form.file.data:
                file = form.file.data
                filename = secure_filename(f"{product.id}.jpg")
                filepath = os.path.join(current_app.config['UPLOADED_FOLDER'], filename)
                file.save(filepath)

            db.session.commit()
            return redirect(url_for('products_blueprint.products'))
        return render_template('modify_product.html', form=form)
    else:
        raise Unauthorized()


@products_blueprint.route('/products/product/<int:idx>')
def product(idx):
    item = Product.query.filter_by(id=idx).first()
    return render_template('product.html', product=item)


@products_blueprint.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    category = request.args.get('category')

    query = db.session.query(Product).join(ProductCategory, Product.id == ProductCategory.product_id).join(Category, ProductCategory.category_id == Category.id)

    if name:
        query = query.filter_by(Product.name.ilike(f'%{name}%'))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if category:
        query = query.filter(Category.name == category)

    products = query.all()

    return render_template('index.html', products=products, categories=Category.query.all())


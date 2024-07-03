import datetime
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import current_user
from models import Order, Cart, CartItem, Product, db

orders_blueprint = Blueprint('orders_blueprint', __name__, template_folder='templates', static_folder='static')


@orders_blueprint.route('/orders')
def orders():
    order = Order.query.filter_by(user_id=current_user.id)
    return render_template('orders.html', orders=order)


@orders_blueprint.route('/orders', methods=["POST"])
def add_order():
    products_id = request.form.getlist('product_id')
    names = request.form.getlist('name')
    amounts = request.form.getlist('quantity')
    prices = request.form.getlist('price')

    cart = [{"product_id": products_id, "name": names, "amount": int(amounts), "price": float(prices)} for products_id, names, amounts, prices in zip(products_id, names, amounts, prices)]

    for item in cart:
        order = Order(date=datetime.date.today(), state="ordinato", total=item["amount"]*item["price"], user_id=current_user.id, product_id=item["product_id"], quantity=item["amount"])
        db.session.add(order)
        db.session.commit()

    return redirect(url_for('orders_blueprint.orders'))

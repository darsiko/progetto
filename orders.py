import datetime
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from models import Order, Cart, CartItem, Product, db

orders_blueprint = Blueprint('orders_blueprint', __name__, template_folder='templates', static_folder='static')


@orders_blueprint.route('/orders')
def orders():
    order = Order.query.filter_by(user_id=current_user.id).all()
    order_with_name = []
    for i in order:
        product = Product.query.filter_by(id=i.product_id).first()
        order_with_name.append({
            'name': product.name,
            'date': i.date,
            'state': i.state,
            'total': i.total,
            'quantity': i.quantity
        })

    return render_template('orders.html', orders=order_with_name)


@orders_blueprint.route('/orders', methods=["POST"])
def add_order():
    products_id = request.form.getlist('product_id')
    names = request.form.getlist('name')
    amounts = request.form.getlist('quantity')
    prices = request.form.getlist('price')

    cart = [{"product_id": products_id, "name": names, "amount": int(amounts), "price": float(prices)} for
            products_id, names, amounts, prices in zip(products_id, names, amounts, prices)]

    for item in cart:
        order = Order(date=datetime.date.today(), state="ordinato", total=item["amount"] * item["price"],
                      user_id=current_user.id, product_id=item["product_id"], quantity=item["amount"])
        db.session.add(order)
        db.session.commit()

    return redirect(url_for('orders_blueprint.orders'))


@orders_blueprint.route('/orders/menage_orders', methods=["GET", "POST"])
def menage_orders():
    if current_user.role == 'seller' or current_user.role == 'admin':
        subquery = db.session.query(Product.id).filter(Product.seller_id == current_user.id).subquery()
        query = db.session.query(Order).filter(Order.product_id.in_(subquery)).all()
        order_with_name = []
        for i in query:
            product = Product.query.filter_by(id=i.product_id).first()
            order_with_name.append({
                'id': i.id,
                'name': product.name,
                'date': i.date,
                'state': i.state,
                'total': i.total,
                'quantity': i.quantity
            })
        return render_template('menage_orders.html', orders=order_with_name)
    else:
        raise Unauthorized


@orders_blueprint.route('/orders/menage_orders/edit_state/<int:idx>', methods=["POST"])
def edit_state(idx):
    if current_user.role == 'seller' or current_user.role == 'admin':
        new_state = request.form.get('new_state')
        order = Order.query.filter_by(id=idx).first()
        if order:
            order.state = new_state
            db.session.commit()
        return redirect(url_for('orders_blueprint.menage_orders'))
    else:
        raise Unauthorized

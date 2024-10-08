from datetime import date
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import Cart, CartItem, Product, db, session

cart_blueprint = Blueprint('cart_blueprint', __name__, template_folder='templates', static_folder='static')


@cart_blueprint.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    current_cart = session.query(Cart).filter_by(user_id=current_user.id).first()
    products_in_cart = []
    if current_cart:
        cart_items = session.query(CartItem, Product).join(Product, CartItem.product_id == Product.id).filter(
            CartItem.cart_id == current_cart.id).all()

        for cart_item, product in cart_items:
            products_in_cart.append({
                'cart_id': cart_item.cart_id,
                'product_id': product.id,
                'name': product.name,
                'description': product.description,
                'quantity': cart_item.quantity,
                'price': product.price
            })

    return render_template('cart.html', cart=products_in_cart)


@cart_blueprint.route('/cart/<int:idx>/add', methods=['POST'])
@login_required
def add_to_cart(idx):
    quantity = request.form.get('quantity', 1)
    carr = Cart.query.filter_by(user_id=current_user.id).first()

    if not carr:
        carr = Cart(last_modified=date.today(), user_id=current_user.id)
        db.session.add(carr)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=carr.id, product_id=idx).first()

    if cart_item:
        cart_item.quantity += int(quantity)
    else:
        cart_item = CartItem(product_id=idx, cart_id=carr.id, quantity=int(quantity))
        db.session.add(cart_item)

    carr.last_modified = date.today()

    db.session.commit()
    return redirect(url_for('cart_blueprint.cart'))


@cart_blueprint.route('/cart/<int:idp>/<int:idc>/remove', methods=['POST'])
@login_required
def remove(idp, idc):
    cart_item = CartItem.query.filter_by(cart_id=idc, product_id=idp).first()
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart_blueprint.cart'))


@cart_blueprint.route('/cart/<int:idp>/<int:idc>/update', methods=['POST'])
@login_required
def update_quantity(idp, idc):
    new_quantity = int(request.form.get('quantity'))
    cart_item = CartItem.query.filter_by(cart_id=idc, product_id=idp).first()
    if cart_item and new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.cart.last_modified = date.today()
        db.session.commit()
    return redirect(url_for('cart_blueprint.cart'))

from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import current_user
from app.models import db, Cart, CartItem, Product

cart_bp = Blueprint('cart', __name__)

def get_or_create_cart():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        return cart
    else:
        # For guests, use session to store cart items
        if 'cart_items' not in session:
            session['cart_items'] = []
        return None

@cart_bp.route('/cart')
def view_cart():
    if current_user.is_authenticated:
        cart = get_or_create_cart()
        cart_items = cart.items if cart else []
    else:
        # For guests, cart_items is a list of dicts in session
        cart_items = []
        for item in session.get('cart_items', []):
            product = Product.query.get(item['product_id'])
            if product:
                cart_items.append(type('CartItem', (), {
                    'product': product,
                    'quantity': item['quantity']
                })())
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 5.00
    total = subtotal + shipping
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, total=total)

@cart_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if current_user.is_authenticated:
        cart = get_or_create_cart()
        item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if item:
            item.quantity += 1
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
            db.session.add(item)
        db.session.commit()
    else:
        # For guests, update session cart
        cart_items = session.get('cart_items', [])
        for item in cart_items:
            if item['product_id'] == product_id:
                item['quantity'] += 1
                break
        else:
            cart_items.append({'product_id': product_id, 'quantity': 1})
        session['cart_items'] = cart_items
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if current_user.is_authenticated:
        cart = get_or_create_cart()
        item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
    else:
        cart_items = session.get('cart_items', [])
        cart_items = [item for item in cart_items if item['product_id'] != product_id]
        session['cart_items'] = cart_items
    return redirect(url_for('cart.view_cart'))
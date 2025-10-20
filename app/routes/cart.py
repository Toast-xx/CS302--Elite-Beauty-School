from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_login import current_user
from ..models import db, Cart, CartItem, Product
from ..utils import *


# Blueprint for cart-related routes
cart_bp = Blueprint('cart', __name__)

# Helper function to get the current user's cart, or create one if it doesn't exist

def get_or_create_cart():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        return cart



@cart_bp.route('/cart')
@require_clearance(1)
def view_cart():
    # Displays the current user's cart with items, subtotal, shipping, and total cost
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    cart = get_or_create_cart()
    cart_items = cart.items if cart else []
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 5.00
    total = subtotal + shipping
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, total=total)

@cart_bp.route('/cart/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Adds a product to the cart or updates quantity if already present
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    quantity = int(request.form.get('quantity', 1))
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/update_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    # Updates the quantity of a specific product in the cart
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 403
    data = request.get_json()
    change = data.get('change', 0)
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity = max(item.quantity + change, 1)
        db.session.commit()
        cost = item.product.price * item.quantity
        return jsonify({'new_quantity': item.quantity, 'cost': cost})
    return jsonify({'error': 'Item not found'}), 404

@cart_bp.route('/cart/delete_item/<int:product_id>', methods=['POST'])
def delete_cart_item(product_id):
    # Removes a product from the cart
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 403
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Item not found'}), 404
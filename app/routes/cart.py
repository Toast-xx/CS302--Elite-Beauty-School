from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from flask_login import current_user
from app.models import db, Cart, CartItem, Product, Order, OrderItem
from app.utils import *
from app.routes.email_handler import send_order_confirmation_email
from ..models import db, Cart, CartItem, Product
from ..utils import *


# Blueprint for cart-related routes
cart_bp = Blueprint('cart', __name__)

def get_or_create_cart():
    """
    Retrieve the current user's cart from the database.
    If the cart does not exist, create a new one.
    Returns:
        Cart object for the current user.
    """
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
    """
    Display the current user's cart with all items, subtotal, shipping, and total.
    Redirects to login if user is not authenticated.
    """
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
    """
    Add a product to the current user's cart.
    If the product is already in the cart, increase its quantity.
    Redirects to login if user is not authenticated.
    """
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
    """
    Update the quantity of a specific product in the cart.
    Expects a JSON payload with 'change' (int).
    Returns updated quantity and cost, or error if not found.
    """
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
    """
    Remove a product from the cart.
    Returns success or error as JSON.
    """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 403
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Item not found'}), 404

@cart_bp.route('/cart/complete_order', methods=['GET', 'POST'])
@require_clearance(1)
def complete_order():
    """
    Complete the current order:
    - Creates an Order and associated OrderItems from the cart
    - Clears the cart
    - Sends a confirmation email with PDF invoice
    - Redirects to the order success page
    If cart is empty, flashes a warning and redirects to cart view.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    cart = get_or_create_cart()
    cart_items = cart.items if cart else []
    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.view_cart'))

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 5.00
    total = subtotal + shipping

    # Create the order
    order = Order(user_id=current_user.id, status="Paid", total=total)
    db.session.add(order)
    db.session.flush()

    # Add order items for each cart item
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)

    # Clear the cart by deleting all items
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    # Send confirmation email with PDF invoice
    send_order_confirmation_email(current_user.email, order)

    return redirect(url_for('cart.order_success'))

@cart_bp.route('/cart/order_success')
@require_clearance(1)
def order_success():
    """
    Render the order success (thank you) page after a completed order.
    """
    return render_template('order_success.html')
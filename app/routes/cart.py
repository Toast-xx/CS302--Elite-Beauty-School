"""
Cart routes: Handles all cart-related operations including viewing, adding, updating,
deleting cart items, and completing orders. Also manages inventory updates for online purchases.
"""

from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from flask_login import current_user
from app.models import db, Cart, CartItem, CampusProduct, Order, OrderItem
from app.utils import *
from app.routes.email_handler import send_order_confirmation_email
from ..models import db, Cart, CartItem, CampusProduct
from ..utils import *
from decimal import Decimal
import logging

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
    # Calculate subtotal and total including shipping
    subtotal = sum(item.campus_product.price * item.quantity for item in cart_items if item.campus_product)
    shipping = Decimal("5.00")
    total = subtotal + shipping
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, total=total)

@cart_bp.route('/cart/add_to_cart/<int:campus_product_id>', methods=['POST'])
def add_to_cart(campus_product_id):
    """
    Add a campus-specific product to the current user's cart.
    If the product is already in the cart, increase its quantity.
    Redirects to login if user is not authenticated.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    quantity = int(request.form.get('quantity', 1))
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, campus_product_id=campus_product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, campus_product_id=campus_product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/update_quantity/<int:campus_product_id>', methods=['POST'])
def update_cart_quantity(campus_product_id):
    """
    Update the quantity of a specific campus product in the cart.
    Expects a JSON payload with 'change' (int).
    Returns updated quantity and cost, or error if not found.
    """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 403
    data = request.get_json()
    change = data.get('change', 0)
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, campus_product_id=campus_product_id).first()
    if item:
        item.quantity = max(item.quantity + change, 1)
        db.session.commit()
        cost = float(item.campus_product.price) * item.quantity
        return jsonify({'new_quantity': item.quantity, 'cost': cost})
    return jsonify({'error': 'Item not found'}), 404

@cart_bp.route('/cart/delete_item/<int:campus_product_id>', methods=['POST'])
def delete_cart_item(campus_product_id):
    """
    Remove a campus product from the cart.
    Returns success or error as JSON.
    """
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 403
    cart = get_or_create_cart()
    item = CartItem.query.filter_by(cart_id=cart.id, campus_product_id=campus_product_id).first()
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
    - Decrements campus_quantity for each purchased product
    - Clears the cart
    - Sends a confirmation email with PDF invoice
    - Renders the order success page
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    cart = get_or_create_cart()
    cart_items = cart.items if cart else []
    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.view_cart'))

    subtotal = sum(item.campus_product.price * item.quantity for item in cart_items if item.campus_product)
    shipping = Decimal("5.00")
    total = subtotal + shipping

    try:
        # Create the order
        order = Order(user_id=current_user.id, status="Paid", total=total)
        db.session.add(order)
        db.session.flush()

        # Add order items for each cart item and decrement campus_quantity
        for item in cart_items:
            if item.campus_product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.campus_product.product_id,
                    campus_product_id=item.campus_product.id,
                    quantity=item.quantity,
                    price=item.campus_product.price
                )
                db.session.add(order_item)
                # Decrement campus_quantity for online purchase
                if item.campus_product.campus_quantity is not None:
                    item.campus_product.campus_quantity -= item.quantity

        # Clear the cart by deleting all items
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()
        logging.info(f"Order {order.id} created for user {current_user.id}")

        # Try to send confirmation email
        try:
            send_order_confirmation_email(current_user.email, order)
        except Exception as mail_error:
            logging.error(f"Order {order.id}: Email sending failed: {mail_error}")
            flash("Order placed, but confirmation email could not be sent.", "warning")

        # Always render the order success page after a successful order
        return render_template('order_success.html', order=order)

    except Exception as e:
        db.session.rollback()
        logging.error(f"Order creation failed: {e}")
        flash("There was an error processing your order. Please try again.", "danger")
        return redirect(url_for('cart.view_cart'))

    return render_template('order_success.html')

@cart_bp.route('/cart/order_success')
@require_clearance(1)
def order_success():
    """
    Render the order success (thank you) page after a completed order.
    """
    return render_template('order_success.html')
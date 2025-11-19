"""
    - Displays all orders for the current user.
    - Eager loads related order items and campus products for efficient template rendering.
    - Integrates with Flask-Login for authentication and session management.
    - Uses SQLAlchemy's joinedload for optimized database queries.
    - Renders the order_history.html template with the user's orders.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Order, OrderItem
from sqlalchemy.orm import joinedload



API_URL = "https://cs-302-elite-beauty-school.vercel.app/"

order_history_bp = Blueprint('order_history', __name__)

@order_history_bp.route('/order_history')
@login_required
def order_history():
    """
    Query all orders for the current user, eager loading order items and campus products,
    and render the order history template.
    """
    orders = (
        Order.query
        .filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .options(
            joinedload(Order.items).joinedload(OrderItem.campus_product)
        )
        .all()
    )
    return render_template('order_history.html', orders=orders, api_url=API_URL)
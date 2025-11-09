"""
Order history route: Displays all orders for the current user,
including eager loading of related order items and campus products.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Order, OrderItem
from sqlalchemy.orm import joinedload

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
    return render_template('order_history.html', orders=orders)
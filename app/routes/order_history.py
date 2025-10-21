from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Order

order_history_bp = Blueprint('order_history', __name__)

@order_history_bp.route('/order_history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order_history.html', orders=orders)
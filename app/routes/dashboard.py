"""
    - Handles the user dashboard view.
    - Integrates with Flask-Login to ensure only authenticated users can access the dashboard.
    - Renders the 'user_dashboard.html' template for the dashboard page.
    - Blueprint is registered as 'dashboard_bp' for modular route management.
"""
from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user_dashboard.html')
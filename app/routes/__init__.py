"""
    - Imports and registers all route blueprints for the application.
    - Centralizes blueprint registration for modular route management.
    - Ensures each feature (main, store, user, auth, product detail, cart, checkout, dashboard, order history, account) is available in the Flask app.
    - Call register_routes(app) in your app factory to attach all routes.
"""
from .admin import admin
from .main import main
from .store import products
from .user import user
from .auth import auth
from .product_detail import product_detail_bp
from .cart import cart_bp
from .checkout import *
from .dashboard import dashboard_bp
from .order_history import order_history_bp
from .account import account_bp

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(product_detail_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(order_history_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(admin)
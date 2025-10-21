from app.routes.main import main
from app.routes.store import products
from app.routes.user import user
from app.routes.auth import auth
from app.routes.product_detail import product_detail_bp
from app.routes.cart import cart_bp
from app.routes.checkout import *
from app.routes.dashboard import dashboard_bp
from app.routes.order_history import order_history_bp
from app.routes.account import account_bp

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
    

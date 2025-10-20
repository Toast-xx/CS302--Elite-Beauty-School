from .main import main
from .store import products
from .user import user
from .auth import auth
from .product_detail import product_detail_bp
from .cart import cart_bp
from .checkout import *

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(product_detail_bp)
    app.register_blueprint(cart_bp)
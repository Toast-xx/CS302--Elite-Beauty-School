from app.routes.main import main
from app.routes.store import products
from app.routes.user import user
from app.routes.auth import auth

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(user)
    app.register_blueprint(auth)
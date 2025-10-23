from app.routes.main import main
from app.routes.store import products  # ← import your new blueprint

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(products)  # ← register the products route

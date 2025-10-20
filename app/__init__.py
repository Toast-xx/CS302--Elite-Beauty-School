from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config

# Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_object=Config):
    # Define app
    app = Flask(__name__)

    # TODO: replace this with random value during deployment
    app.secret_key = 'Placeholder_Secret_Key'

    # Load configuration
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models so Alembic sees them
    from app import models
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes/blueprints
    from .routes import register_routes
    register_routes(app)

    return app
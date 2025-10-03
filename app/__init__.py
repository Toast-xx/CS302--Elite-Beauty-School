from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object=Config):
    # Define app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so Alembic sees them
    from app import models

    # Register routes/blueprints
    from .routes import register_routes
    register_routes(app)

    return app

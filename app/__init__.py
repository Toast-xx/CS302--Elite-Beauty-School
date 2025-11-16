"""
Flask application factory and extension initialization.
Sets up database, migrations, login manager, mail, and blueprint registration.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config
from flask_mail import Mail
from flask_cors import CORS
import stripe
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask extensions (used throughout the app)
db = SQLAlchemy()         # Database ORM
migrate = Migrate()       # Database migrations
login_manager = LoginManager()  # User session management
mail = Mail()             # Email sending

def create_app(config_object=Config):
    """
    Application factory function.
    Creates and configures the Flask app instance, initializes extensions,
    registers blueprints, and sets up user loading for authentication.

    Args:
        config_object: The configuration object to use (default: Config).

    Returns:
        app: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Enable CORS for your Vercel frontend
    CORS(app,supports_credentials=True, origins=["https://elite-emporium-omega.vercel.app/"])  # Replace with your actual Vercel domain

    # Register all route blueprints
    from .routes import register_routes
    register_routes(app)

    # Initialize Stripe API key
    stripe.api_key = os.environ.get("STRIPE_API_KEY")

    # Create the Flask app instance
    app = Flask(__name__)

    # Set the secret key for session management and CSRF protection
    # TODO: Replace this with a secure, random value in production
    app.secret_key = 'FLASK_SECRET_KEY'

    # Load configuration from the provided config object (e.g., from .env)
    app.config.from_object(config_object)

    # Initialize Flask extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Endpoint for @login_required redirects
    mail.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import models so Alembic can detect them for migrations
    from app import models
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback to reload the user object from the user ID stored in the session.
        Used by Flask-Login for user session management.
        """
        return User.query.get(int(user_id))

    # Register all application routes and blueprints
    from .routes import register_routes
    register_routes(app)

    return app

# Optionally expose app for Gunicorn if you want to run with gunicorn app:app
app = create_app()
"""
    - Handles authentication and user management for the application.
    - Integrates with Flask-Login via UserMixin for session management.
    - Stores user information, password hash, clearance level, and campus relationship.
    - Provides helper methods for user creation and lookup.
    - Handles database integrity errors and returns clear status messages.
    - Used throughout the app for login, registration, and user-related queries.
"""

from flask_login import UserMixin
from enum import Enum
from app import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    clearance_level = db.Column(db.Integer, nullable=False, default=1) # highest clearance is 3

    campus_id = db.Column(db.BigInteger, db.ForeignKey("campuses.id"), nullable=True)
    campus = db.relationship("Campus", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"<User {self.name}, email={self.email}, clearance={self.clearance_level}>"

    def to_dict(self):
        # Converts user instance to dictionary for API or template use
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "clearance_level": self.clearance_level,
            "campus_id": self.campus_id,
        }

    @classmethod
    def add_new_user(cls, name, email, password_hash, clearance_level=1, campus_id=None) -> tuple:
        """
        Create and add a new user to the database.

        Returns:
            tuple: (user, message)
        """
        # Validate clearance range
        if clearance_level not in [1, 2, 3]:
            return None, "Invalid clearance level. Must be 1, 2, or 3."

        new_user = cls(
            name=name,
            email=email.lower().strip(),
            password_hash=password_hash,
            clearance_level=clearance_level,
            campus_id=campus_id,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user, "User added successfully."
        except db.IntegrityError:
            db.session.rollback()
            return None, "Email already exists."
        except Exception as e:
            db.session.rollback()
            return None, f"An error occurred: {e}"

    @classmethod
    def get_user_by_email(cls, email: str) -> tuple:
        """
        Retrieve a user by their email address.

        Returns:
            tuple: (user, message)
        """
        user = cls.query.filter_by(email=email).first()
        if user:
            return user, "User found."
        return None, "User not found."
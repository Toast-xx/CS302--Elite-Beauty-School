"""
    - Handles authentication and user management for the application.
    - Integrates with Flask-Login via UserMixin for session management.
    - Stores user information, password hash, clearance level, and campus relationship.
    - Provides helper methods for user creation and lookup.
    - Handles database integrity errors and returns clear status messages.
    - Used throughout the app for login, registration, and user-related queries.
"""

from flask_login import UserMixin
from app import db
from sqlalchemy import Date
from datetime import date

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    clearance_level = db.Column(db.Integer, nullable=False, default=1) # highest clearance is 3
    start_date = db.Column(Date, nullable=True)
    end_date = db.Column(Date, nullable=True)
    campus_id = db.Column(db.BigInteger, db.ForeignKey("campuses.id"), nullable=True)
    campus = db.relationship("Campus", backref=db.backref("users", lazy=True))
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}, email={self.email}, clearance={self.clearance_level}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "clearance_level": self.clearance_level,
            "campus_id": self.campus_id,
            "campus": self.campus,
            "start_date": str(self.start_date) if self.start_date else None,
            "end_date": str(self.end_date) if self.end_date else None,
            "active": self.active
        }

    @classmethod
    def add_new_user(cls, name, email, password_hash, clearance_level=1, campus_id=None, start_date=None, end_date=None, active=True):
        if clearance_level not in [1, 2, 3]:
            return None, "Invalid clearance level. Must be 1, 2, or 3."

        new_user = cls(
            name=name,
            email=email.lower().strip(),
            password_hash=password_hash,
            clearance_level=clearance_level,
            campus_id=campus_id,
            start_date=start_date,
            end_date=end_date,
            
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
    def get_user_by_email(cls, email: str):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user, "User found."
        return None, "User not found."
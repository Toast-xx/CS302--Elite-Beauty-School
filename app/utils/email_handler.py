"""
Email validation and uniqueness checking utilities.

- Provides functions to validate email format using regex.
- Checks if an email is already in use in the database.
- Used for user registration and profile updates to ensure email integrity.
"""

import re
from flask import current_app
from app.models import User
from app import db

# Regex pattern for validating email addresses (RFC-like, no double dots, length limits)
EMAIL_REGEX = re.compile(
    r"^(?=.{6,254}$)(?!.*\.\.)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def is_valid_email(email: str) -> bool:
    """
    Checks if the provided email string matches the valid email pattern.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(EMAIL_REGEX.match(email.lower().strip()))

def is_email_in_use(email: str, user_id=None) -> bool:
    """
    Checks if the email is already used by another user in the database.

    Args:
        email (str): The email address to check.
        user_id (int, optional): If provided, ignores the user with this ID.

    Returns:
        bool: True if email is in use by another user, False otherwise.
    """
    with current_app.app_context():
        existing_user = db.session.query(User).filter_by(email=email.lower().strip()).first()
        if existing_user:
            # If editing, allow the same user to keep their email
            if user_id is not None and existing_user.id == user_id:
                return False  # Not "in use" for this user
            return True
        return False

def validate_new_email(email: str, user_id=None) -> tuple[bool, str]:
    """
    Validates the email format and checks for uniqueness.

    Args:
        email (str): The email address to validate.
        user_id (int, optional): If provided, ignores the user with this ID.

    Returns:
        tuple: (bool, str) where bool is True if valid and available, and str is a message.
    """
    email = email.lower().strip()
    if not is_valid_email(email):
        return False, "Invalid email format."
    if is_email_in_use(email, user_id):
        return False, "Email is already in use."
    return True, "Email is valid and available."
import re
from flask import current_app
from app.models import User
from app import db

# Email Regex
EMAIL_REGEX = re.compile(
    r"^(?=.{6,254}$)(?!.*\.\.)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def is_valid_email(email: str) -> bool:
    """
    Validate email format using regex.
    Returns True if valid, False otherwise.
    """
    return bool(EMAIL_REGEX.match(email))


def is_email_in_use(email: str) -> bool:
    """
    Check if the email already exists in the database.
    Returns True if the email is taken, False otherwise.
    """
    # Requires an application context to access the DB
    with current_app.app_context():
        existing_user = db.session.query(User).filter_by(email=email).first()
        return existing_user is not None


def validate_new_email(email: str) -> tuple[bool, str]:
    """
    Combined validation: checks format and uniqueness.
    Returns (is_valid, message)
    """
    if not is_valid_email(email):
        return False, "Invalid email format."

    if is_email_in_use(email):
        return False, "Email is already in use."

    return True, "Email is valid and available."

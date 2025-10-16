from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User

def require_clearance(required_level):
    """
    A decorator to ensure a user is logged in and has sufficient security clearance.
    Usage: @require_clearance(3)
    """

    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            user_id = session.get('user_id')  # store only user.id in session
            if not user_id:
                return redirect(url_for('auth.login'))

            # Fetch user from database
            user = User.query.get(user_id)
            if not user:
                return redirect(url_for('auth.login'))

            # Check security clearance level
            if getattr(user, 'clearance_level', 0) < required_level:
                return redirect(url_for('main.home'))

            # Passed both checks
            return f(*args, **kwargs)

        return wrapped_function

    return decorator

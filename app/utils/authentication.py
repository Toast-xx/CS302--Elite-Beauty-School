from functools import wraps
from flask import session, redirect, url_for, flash

def require_clearance(required_level):
    """
    A decorator to ensure a user is logged in and has sufficient security clearance.
    Usage: @require_clearance(3)
    """

    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            # Check login session
            user = session.get('user')
            if not user:
                return redirect(url_for('auth.login'))
            # Check security clearance level
            user_clearance = user.get('clearance_level', 0)
            if user_clearance < required_level:
                return redirect(url_for('main.home'))

            # Passed both checks
            return f(*args, **kwargs)
        return wrapped_function
    return decorator

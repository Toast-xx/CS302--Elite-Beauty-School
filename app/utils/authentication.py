"""
Authentication and authorization utilities.

- Provides the require_clearance decorator for route protection.
- Ensures users are logged in, have sufficient clearance, and are active.
- Used to restrict access to admin/superadmin routes and enforce account status.
"""

from functools import wraps
from flask import session, redirect, url_for, flash, render_template
from app.models import User

def require_clearance(required_level):
    """
    Decorator to restrict route access based on user clearance level and account status.

    Args:
        required_level (int): Minimum clearance level required to access the route.

    Usage:
        @require_clearance(3)  # Only superadmins (level 3) can access

    Returns:
        function: Wrapped route function with access checks.
    """
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                # Redirect to login if not authenticated
                return redirect(url_for('auth.login'))

            user = User.query.get(user_id)
            if not user:
                # Redirect to login if user not found
                return redirect(url_for('auth.login'))

            # Check security clearance level
            if getattr(user, 'clearance_level', 0) < required_level:
                # Redirect to home if insufficient clearance
                return redirect(url_for('main.home'))

            # Check if user is active (start_date <= today <= end_date)
            if not user.is_active:
                # Render inactive account template if not active
                return render_template("inactive_account.html"), 403

            # All checks passed; proceed to route
            return f(*args, **kwargs)
        return wrapped_function
    return decorator
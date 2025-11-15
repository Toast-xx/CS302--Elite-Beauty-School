from flask import Blueprint, jsonify, request, session, render_template, redirect
from flask_login import login_user, logout_user
from app.models import User
from ..utils import *
from ..utils.email_handler import is_valid_email
from ..utils.password_handler import hash_password, verify_password

# Blueprint for authentication routes
auth = Blueprint("auth", __name__)

@auth.route("/auth/login", methods=["GET","POST"])
def login():
    """
    Handles user login via GET and POST requests.
    - GET: Renders the login page.
    - POST: Validates credentials, logs in user, and redirects based on clearance level.
    """
    if request.method == "POST":
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            # Validate email format
            if not is_valid_email(email):
                return render_template("login.html", error="Invalid Email."), 400

            # Retrieve user by email
            user, message = User.get_user_by_email(email)

            if not user:
                return render_template("login.html", error=message), 401

            # Verify password
            if not verify_password(user.password_hash, password):
                return render_template("login.html", error="Incorrect Password."), 401

            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.name
            session['clearance_level'] = getattr(user, 'clearance_level', 1)
            session['campus']=user.campus.name

            login_user(user)

            # Redirect based on clearance level
            if session['clearance_level'] == 2:
                return redirect("/admin")
            elif session['clearance_level'] == 1:
                return redirect("/")
            elif session['clearance_level'] == 3:
                return redirect("/superadmin_dashboard")

            return redirect("/")

        except Exception as e:
            # Handle unexpected errors
            return render_template("login.html", error=e), 401

    # GET request: render login page
    return render_template("login.html"), 200

@auth.route("/auth/logout", methods=["GET"])
def logout():
    """
    Logs out the current user and clears session data.
    Renders the login page with a logout message.
    """
    try:
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('clearance_level', None)
        logout_user()
        return render_template("login.html", message="Logout Successful."), 200
    except Exception as e:
        # Handle unexpected errors during logout
        return render_template("login.html", error=e), 500
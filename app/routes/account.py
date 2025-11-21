"""
    - Handles user account details view and update functionality.
    - Allows users to update their name, email, and password.
    - Integrates with Flask-Login for authentication and session management.
    - Uses utility functions for email validation and password hashing.
    - Commits changes to the database and provides user feedback via flash messages.
    - Renders the account.html template with current user data.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.email_handler import validate_new_email
from app.utils.password_handler import hash_password
from app import db

API_URL = "https://cs302-elite-beauty-school.onrender.com"

account_bp = Blueprint('account', __name__)

@account_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == "POST":
        new_name = request.form.get("name")
        new_email = request.form.get("email")
        new_password = request.form.get("password")

        updated = False

        if new_name and new_name != current_user.name:
            current_user.name = new_name
            updated = True

        if new_email and new_email != current_user.email:
            email_valid, message = validate_new_email(new_email)
            if not email_valid:
                flash(message, "error")
                return redirect(url_for("account.account"))
            current_user.email = new_email
            updated = True

        if new_password:
            current_user.password_hash = hash_password(new_password)
            updated = True

        if updated:
            db.session.commit()
            flash("Account updated successfully.", "success")
        else:
            flash("No changes made.", "info")

        return redirect(url_for("account.account"))

    return render_template("account.html", user=current_user, api_url=API_URL)
"""
Admin routes for user management and search functionality.

- Restricts access to admin users (clearance_level >= 2).
- Provides dashboard, user search, and add/edit user endpoints.
- Handles form validation, error reporting, and database updates.
"""

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session
from app.utils import require_clearance
from app.utils import *
from app.models.user import User  
from app import db
from app.utils.password_handler import hash_password
from datetime import date

# Blueprint for admin-related routes
admin = Blueprint("admin", __name__)

@admin.route("/admin")
@require_clearance(2)  # Only users with clearance_level >= 2 can access
def admin_base():
    """
    Renders the admin dashboard with a list of all users.
    Only accessible to admins.
    """
    # Only allow admins to access the admin dashboard
    if session.get('clearance_level') != 2:
        return redirect("/")
    users = User.query.all()  # Query all users
    return render_template("admin_base.html", items=users, today=date.today())  # Pass users to the template

@admin.route("/searchAdmin", methods=['GET'])
def search_user():
    """
    Searches for users with clearance_level == 1 (students) by name, email, or campus.
    Returns a JSON list of matching users.
    """
    query = request.args.get("q", "").strip()
    campus_id = request.args.get("campus_id", "").strip()

    if not query and not campus_id:
        return jsonify({"error": "No search query provided"}), 400

    try:
        filters = [User.clearance_level == 1]
        if query:
            filters.append(
                (User.name.ilike(f"%{query}%")) |
                (User.email.ilike(f"%{query}%"))
            )
        if campus_id:
            filters.append(User.campus_id == campus_id)

        users = User.query.filter(*filters).all()
        user_list = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "campus_id": user.campus_id,
            }
            for user in users
        ]
        return jsonify(user_list)
    except Exception as ex:
        print(f"Error in /searchAdmin: {ex}")
        return jsonify({"error": "Internal server error"}), 500

# --- Add/Edit User Route ---
@admin.route("/admin/add_user", methods=["POST"])
@require_clearance(2)
def add_user():
    """
    Adds a new user or edits an existing user.
    Validates form fields and handles database updates.
    Renders the admin dashboard with error messages if validation fails.
    """
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    campus_id = request.form.get("campus_id")
    clearance_level = int(request.form.get("clearance_level", 1))
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    # Validate required fields
    if not all([name, email, campus_id]):
        users = User.query.all()
        return render_template("admin_base.html", error="All fields are required", items=users), 400

    if user_id:
        # Edit existing user
        user = User.query.get(user_id)
        if not user:
            users = User.query.all()
            return render_template("admin_base.html", error="User not found", items=users), 404
        # Only block email if it belongs to another user
        existing_user = User.query.filter_by(email=email).first()
        if user.email != email and existing_user and existing_user.id != user.id:
            users = User.query.all()
            return render_template("admin_base.html", error="User with this email already exists", items=users), 400
        # Update user fields
        user.name = name
        user.email = email
        user.campus_id = campus_id
        user.clearance_level = clearance_level
        user.start_date = start_date
        user.end_date = end_date
        if password:
            user.password_hash = hash_password(password)
    else:
        # Add new user
        if User.query.filter_by(email=email).first():
            users = User.query.all()
            return render_template("admin_base.html", error="User with this email already exists", items=users), 400
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            campus_id=campus_id,
            clearance_level=clearance_level,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(user)
    try:
        db.session.commit()
        return redirect(url_for('admin.admin_base', success=1))
    except Exception as ex:
        # Rollback and report error
        db.session.rollback()
        users = User.query.all()
        return render_template("admin_base.html", error="Failed to save user", items=users), 500
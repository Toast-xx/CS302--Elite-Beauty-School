"""
User management routes for the application.

- Handles listing, adding, and editing users.
- Validates input, checks for email uniqueness, and manages user roles and campus assignment.
- Returns JSON responses for AJAX integration with the frontend.
- All routes require admin clearance (level 2).
"""

from flask import Blueprint, jsonify, request, render_template
from ..utils import *
from ..utils.email_handler import is_valid_email, validate_new_email
from ..utils.password_handler import hash_password
from ..models import User
from app import db
from datetime import datetime
from datetime import date

# Blueprint for user management routes
user = Blueprint("user", __name__)

@user.route("/user/list", methods=["GET"])
@require_clearance(2)
def list_users():
    """
    Lists all users for admin view.
    Renders the users.html template with user data.
    """
    users = User.query.all()
    return render_template("users.html", items=users, today=date.today())

@user.route("/user/add", methods=["POST"])
@require_clearance(2)
def add_user():
    """
    Adds a new user to the database.
    Validates input fields, checks for email uniqueness, and hashes password.
    Handles 'Inactive' checkbox logic:
      - If checked, user is inactive (active=False)
      - If unchecked, user is active (active=True)
    Returns a JSON response with success or error message.
    """
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get('email', "").strip()
        password = request.form.get('password', "")

        campus_id_str = request.form.get('campus_id', None)
        if not campus_id_str or not campus_id_str.isdigit():
            return jsonify({"error": "Campus is required and must be a valid ID."}), 400
        campus_id = int(campus_id_str)

        # Validate required fields
        if not name:
            return jsonify({"error": "Name is required."}), 400
        if not email:
            return jsonify({"error": "Email is required."}), 400
        if not password or len(password) < 6:
            return jsonify({"error": "Password is required and must be at least 6 characters."}), 400

        clearance_str = request.form.get('clearance_level', '1')
        if not clearance_str.isdigit() or int(clearance_str) not in [1, 2, 3]:
            return jsonify({"error": "Invalid clearance level. Must be 1, 2, or 3."}), 400
        clearance = int(clearance_str)

        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        # Parse start and end dates if provided
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # Validate email format and uniqueness
        email_valid, message = validate_new_email(email)
        if not email_valid:
            return jsonify({"error": message}), 403

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already in use."}), 400

        hashed_password = hash_password(password)

        # Handle 'Inactive' checkbox logic:
        # If checked, value is '0' (inactive); if unchecked, value is None (active)
        active_raw = request.form.get('active')
        active = False if active_raw == '0' else True

        new_user, message = User.add_new_user(
            name, email, hashed_password, clearance, campus_id, start_date, end_date, active
        )
        if new_user:
            return jsonify({"message": message, "user": new_user.to_dict()}), 201
        else:
            return jsonify({"error": message}), 400

    except Exception as e:
        # Log and return unexpected errors
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@user.route("/user/edit/<int:user_id>", methods=["POST"])
@require_clearance(2)
def edit_user(user_id):
    """
    Edits an existing user's details.
    Validates input, checks for email uniqueness, and updates password if provided.
    Handles 'Inactive' checkbox logic:
      - If checked, user is inactive (active=False)
      - If unchecked, user is active (active=True)
    Returns a JSON response with success or error message.
    """
    try:
        user_obj = User.query.get_or_404(user_id)
        name = request.form.get("name", "").strip()
        email = request.form.get('email', "").strip()
        password = request.form.get('password', "")

        campus_id_str = request.form.get('campus_id', None)
        if not campus_id_str or not campus_id_str.isdigit():
            return jsonify({"error": "Campus is required and must be a valid ID."}), 400
        campus_id = int(campus_id_str)

        # Validate required fields
        if not name:
            return jsonify({"error": "Name is required."}), 400
        if not email:
            return jsonify({"error": "Email is required."}), 400
        if password and len(password) < 6:
            return jsonify({"error": "Password is required and must be at least 6 characters."}), 400

        clearance_str = request.form.get('clearance_level', '1')
        if not clearance_str.isdigit() or int(clearance_str) not in [1, 2, 3]:
            return jsonify({"error": "Invalid clearance level. Must be 1, 2, or 3."}), 400
        clearance = int(clearance_str)

        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        # Parse start and end dates if provided
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # Pass user_id to validation so user's own email is allowed
        email_valid, message = validate_new_email(email, user_id=user_obj.id)
        if not email_valid:
            return jsonify({"error": message}), 403

        existing_user = User.query.filter_by(email=email).first()
        if user_obj.email != email and existing_user and existing_user.id != user_obj.id:
            return jsonify({"error": "Email already in use."}), 400

        # Handle 'Inactive' checkbox logic:
        # If checked, value is '0' (inactive); if unchecked, value is None (active)
        active_raw = request.form.get('active')
        user_obj.active = False if active_raw == '0' else True

        # Update user fields
        user_obj.name = name
        user_obj.email = email
        user_obj.campus_id = campus_id
        user_obj.clearance_level = clearance
        user_obj.start_date = start_date
        user_obj.end_date = end_date
        if password:
            user_obj.password_hash = hash_password(password)
        try:
            db.session.commit()
            return jsonify({"message": "User details updated successfully!", "user": user_obj.to_dict()}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    except Exception as e:
        # Log and return unexpected errors
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
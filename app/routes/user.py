from flask import Blueprint, jsonify, request, session, render_template, redirect
from app.utils import *
from app.utils.email_handler import is_valid_email, validate_new_email
from app.utils.password_handler import hash_password
from app.models import User

user = Blueprint("user", __name__)


@user.route("/user/add", methods=["POST"])
@require_clearance(2)
def add_user():
    try:
        name = request.form.get("name")
        email = request.form.get('email')
        password = request.form.get('password')
        clearance = request.form.get('clearance', 1)
        campus_id = request.form.get('campus_id')

        email_valid, message = validate_new_email(email) # validate email in utils/email_handler, returns tuple

        if email_valid:
            pass
        else:
            return jsonify({"error": message}), 403

        hashed_password = hash_password(password)

        new_user, message = User.add_new_user(name, email, hashed_password, clearance, campus_id)

        if new_user:
            return jsonify({"message": message, "user": new_user.to_dict()}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


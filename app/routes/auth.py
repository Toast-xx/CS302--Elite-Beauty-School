from flask import Blueprint, jsonify, request, session, render_template, redirect
from app.models import User
from app.utils import *
from app.utils.email_handler import is_valid_email
from app.utils.password_handler import hash_password, verify_password

auth = Blueprint("auth", __name__)


@auth.route("/auth/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            if is_valid_email(email):
                pass
            else:
                return jsonify({"error": "Invalid Email."}), 400

            user, message = User.get_by_email(email)

            if user:
                pass
            else:
                return jsonify({"error": message}), 401

            if verify_password(password, user.password):
                pass
            else:
                return jsonify({"error": "Incorrect Password."}), 401

            session['user'] = user

            return redirect("/"), 200 # TODO: add render template for home page

        except Exception as e:
            return jsonify({"error": f"Login Failed: {e}"}, 401)

    # If method is GET
    return render_template("login.html"), 200 # TODO: add render template for login


@auth.route("/auth/logout", methods=["GET","POST"])
def logout():
    try:
        session.pop('user', None)

        return jsonify({"message": "Logout Successful."}, 200)
    except Exception as e:
        return jsonify({"error": f"Logout Failed: {e}"}, 500)

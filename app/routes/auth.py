from flask import Blueprint, jsonify, request, session, render_template, redirect
from flask_login import login_user, logout_user
from app.models import User
from ..utils import *
from ..utils.email_handler import is_valid_email
from ..utils.password_handler import hash_password, verify_password

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
                return render_template("login.html", error="Invalid Email."), 400

            user, message = User.get_user_by_email(email)

            if user:
                pass
            else:
                return render_template("login.html", error=message), 401

            if verify_password(user.password_hash, password):
                 pass
                
            else:
                return render_template("login.html", error="Incorrect Password."), 401

            session['user_id'] = user.id
            session['username'] = user.name
            
            login_user(user)

            return redirect("/")

        except Exception as e:
            return render_template("login.html", error=e), 401

    # If method is GET
    return render_template("login.html"), 200


@auth.route("/auth/logout", methods=["GET"])
@require_clearance(1)
def logout():
    try:
        session.pop('user_id', None)

        logout_user()

        return render_template("login.html", message="Logout Successful."), 200
    except Exception as e:
        return render_template("login.html", error=e), 500

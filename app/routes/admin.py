from flask import Blueprint, jsonify, request
from app.utils import *
from app.models.user import User  # ✅ import your User model

admin = Blueprint("admin", __name__)

@admin.route("/searchAdmin", methods=['GET'])
def search_user():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        users = (
            User.query
            .filter(User.clearance_level == 1)  # same logic as role='student'
            .filter(User.name.ilike(f"%{query}%"))  # case-insensitive match
            .all()
        )
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

from flask import jsonify,request, Blueprint, render_template
from app.utils import *

admin = Blueprint("admin", __name__)

@admin.route("/searchUser",methods=['GET'])
def searchUser():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    search_pattern = f"%{query}%"
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT user.id, user.name
            FROM user
            WHERE user.role = 'student' AND user.name LIKE ?;
        """,
            (search_pattern,),
        )
        results = cursor.fetchall()

        user = []
        for row in results:
            id,name= row
            user.append(
                {
                    "name": name,
                    "id": id,
                }
            )

        return jsonify(user)

    except Exception as ex:
        return jsonify({"error": "Internal server error"}), 500

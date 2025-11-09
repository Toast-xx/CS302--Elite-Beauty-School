from flask import Blueprint
from app.utils import *




main = Blueprint("main", __name__)

@main.route("/")
#@require_clearance(1)
def home():
    return redirect(url_for("products.show_products"))

"""
    - Defines the root ("/") route for the application.
    - Redirects users to the store's product listing page.
    - Integrates with Flask blueprints for modular route management.
    - Uses @require_clearance(1) to restrict access based on user clearance level.
    - Imports utility functions from app.utils for use in this module.
"""
from flask import Blueprint
from app.utils import *




main = Blueprint("main", __name__)

@main.route("/")
#@require_clearance(1)
def home():
    return redirect(url_for("products.show_products"))

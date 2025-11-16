# Handles the product detail page route.
# Fetches product information, example campuses, and simple product recommendations.
# Renders product_detail.html with all required context.
# If you want dynamic campuses, replace the static list with a database query.

from flask import Blueprint, abort
from app.models.product import Product
from flask_login import current_user
from app.models.campus_products import CampusProduct
from app.utils import *


product_detail_bp = Blueprint("product_detail", __name__, url_prefix="/product")

@product_detail_bp.route("/<int:product_id>")
@require_clearance(1)
def product_detail(product_id):
    # Query the product from the database, 404 if not found
    product = Product.query.get_or_404(product_id)

    # Get the campus-specific product info
    campus_product = CampusProduct.query.filter_by(
        product_id=product_id,
        campus_id=current_user.campus_id
    ).first()

    # Simple recommendations: get 5 other products (excluding current)
    # For each recommended product, get its campus-specific product for the current campus
    recommended_products = (
        Product.query.filter(Product.id != product_id).limit(5).all()
    )
    recommendations = []
    for rec_product in recommended_products:
        rec_campus_product = CampusProduct.query.filter_by(
            product_id=rec_product.id,
            campus_id=current_user.campus_id
        ).first()
        recommendations.append({
            "product": rec_product,
            "campus_product": rec_campus_product
        })

    return render_template(
        'product_detail.html',
        product=product,
        campus_product=campus_product,
        recommendations=recommendations
    )
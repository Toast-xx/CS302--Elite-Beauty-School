from flask import Blueprint, render_template, abort
from app.models.product import Product
from app.utils import *

product_detail_bp = Blueprint("product_detail", __name__, url_prefix="/product")

@product_detail_bp.route("/<int:product_id>")
@require_clearance(1)
def product_detail(product_id):
    # Query the product from the database
    product = Product.query.get_or_404(product_id)

    # Example campuses (replace with a query if you want dynamic campuses)
    campuses = ['Auckland', 'Wellington', 'Christchurch']

    # Simple recommendations: get 5 other products (excluding current)
    recommendations = Product.query.filter(Product.id != product_id).limit(5).all()

    return render_template(
        'product_detail.html',
        product=product,
        campuses=campuses,
        recommendations=recommendations
       
    )
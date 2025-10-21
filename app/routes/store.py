# Handles product listing, filtering, and AJAX-based updates for the store page.
# Provides both full page rendering and partial product grid rendering for dynamic updates.
# Depends on Product, Category, and SubCategory models, and expects store.html template and AJAX requests from store.js.

from flask import Blueprint, render_template, render_template_string, request
from app.models.product import Product
from app.models.category import Category, SubCategory
from app.models.campus_products import CampusProduct
from flask_login import current_user
from app.utils import *
from ..models.product import Product
from ..models.category import Category, SubCategory
from ..utils import *


products = Blueprint("products", __name__, url_prefix="/store")

@products.route("/")
@require_clearance(1)
def show_products():
    category_id = request.args.get("category", type=int)
    subcategory_id = request.args.get("subcategory", type=int)
    brand = request.args.get("brand")
    ajax = request.args.get("ajax", type=int)

    categories = Category.query.all()
    subcategories = []
    campus_products_query = CampusProduct.query.join(Product, CampusProduct.product_id == Product.id)\
        .filter(CampusProduct.campus_id == current_user.campus_id)

    if category_id:
        subcategories = SubCategory.query.filter_by(category_id=category_id).all()
    if subcategory_id:
        campus_products_query = campus_products_query.filter(Product.sub_category_id == subcategory_id)
    else:
        subcat_ids = [sc.id for sc in subcategories]
        if subcat_ids:
            campus_products_query = campus_products_query.filter(Product.sub_category_id.in_(subcat_ids))
    if brand:
        campus_products_query = campus_products_query.filter(Product.brand == brand)

    campus_products = campus_products_query.all()
    brands = [row[0] for row in Product.query.with_entities(Product.brand).distinct() if row[0]]

    if ajax:
        return render_template_string("""
        <div class="row">
            {% for cp in campus_products %}
            <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
                <a href="{{ url_for('product_detail.product_detail', product_id=cp.product.id) }}" style="text-decoration: none; color: inherit;">
                    <div class="card h-100 shadow-sm position-relative">
                        {% if cp.product.image_gallery and cp.product.image_gallery[0].startswith('http') %}
                        <img src="{{ cp.product.image_gallery[0] }}" class="card-img-top product-img" alt="{{ cp.product.name }}">
                        {% elif cp.product.image_gallery %}
                        <img src="{{ url_for('static', filename='images/' ~ cp.product.image_gallery[0]) }}" class="card-img-top product-img" alt="{{ cp.product.name }}">
                        {% else %}
                        <img src="{{ url_for('static', filename='images/placeholder.png') }}" class="card-img-top product-img" alt="No image">
                        {% endif %}
                        <div class="card-body">
                            <h5 class="card-title">{{ cp.product.name }}</h5>
                            <p class="card-text mb-1"><strong>Brand:</strong> {{ cp.product.brand }}</p>
                            <p class="card-text mb-1"><strong>Price:</strong> NZD ${{ "%.2f"|format(cp.price) }}</p>
                            <p class="card-text mb-1"><strong>Quantity:</strong> {{ cp.campus_quantity }}</p>
                        </div>
                    </div>
                </a>
            </div>
            {% endfor %}
        </div>
        """, campus_products=campus_products)
    else:
        return render_template(
            "store.html",
            campus_products=campus_products,
            categories=categories,
            subcategories=subcategories,
            brands=brands,
            selected_category=category_id,
            selected_subcategory=subcategory_id,
            selected_brand=brand,
        )
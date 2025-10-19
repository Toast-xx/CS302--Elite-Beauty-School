# Handles product listing, filtering, and AJAX-based updates for the store page.
# Provides both full page rendering and partial product grid rendering for dynamic updates.
# Depends on Product, Category, and SubCategory models, and expects store.html template and AJAX requests from store.js.

from flask import Blueprint, render_template, render_template_string, request
from app.models.product import Product
from app.models.category import Category, SubCategory
from app.utils import *

products = Blueprint("products", __name__, url_prefix="/store")

@products.route("/")
@require_clearance(1)
def show_products():
    # Extract filter parameters from query string
    category_id = request.args.get("category", type=int)
    subcategory_id = request.args.get("subcategory", type=int)
    brand = request.args.get("brand")
    ajax = request.args.get("ajax", type=int)

    categories = Category.query.all()
    subcategories = []
    products_query = Product.query

    # Filter products by category and subcategory
    if category_id:
        subcategories = SubCategory.query.filter_by(category_id=category_id).all()
        if subcategory_id:
            products_query = products_query.filter_by(sub_category_id=subcategory_id)
        else:
            subcat_ids = [sc.id for sc in subcategories]
            if subcat_ids:
                products_query = products_query.filter(Product.sub_category_id.in_(subcat_ids))
    # Filter products by brand
    if brand:
        products_query = products_query.filter_by(brand=brand)

    products = products_query.all()
    brands = [row[0] for row in Product.query.with_entities(Product.brand).distinct() if row[0]]

    if ajax:
        # For AJAX requests, only render the product grid HTML
        return render_template_string("""
        <div class="row">
            {% for product in products %}
            <div class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
                <a href="{{ url_for('product_detail.product_detail', product_id=product.id) }}" style="text-decoration: none; color: inherit;">
                    <div class="card h-100 shadow-sm position-relative">
                        {% if product.image_gallery and product.image_gallery[0].startswith('http') %}
                        <img src="{{ product.image_gallery[0] }}" class="card-img-top product-img" alt="{{ product.name }}">
                        {% elif product.image_gallery %}
                        <img src="{{ url_for('static', filename='images/' ~ product.image_gallery[0]) }}" class="card-img-top product-img" alt="{{ product.name }}">
                        {% else %}
                        <img src="{{ url_for('static', filename='images/placeholder.png') }}" class="card-img-top product-img" alt="No image">
                        {% endif %}
                        <div class="card-body">
                            <h5 class="card-title">{{ product.name }}</h5>
                            <p class="card-text mb-1"><strong>Brand:</strong> {{ product.brand }}</p>
                            <p class="card-text mb-1"><strong>Price:</strong> NZD ${{ "%.2f"|format(product.price) }}</p>
                        </div>
                    </div>
                </a>
            </div>
            {% endfor %}
        </div>
        """, products=products)
    else:
        # For normal requests, render the full store page
        return render_template(
            "store.html",
            products=products,
            categories=categories,
            subcategories=subcategories,
            brands=brands,
            selected_category=category_id,
            selected_subcategory=subcategory_id,
            selected_brand=brand,
        )
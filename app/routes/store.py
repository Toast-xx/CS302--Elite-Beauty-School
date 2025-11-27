# Adds search bar logic to existing product filtering and live search suggestions (autocomplete)
# Now supports autocomplete for product name, category, subcategory, and brand

from flask import Blueprint, render_template_string, request, jsonify
from app.models.product import Product
from app.models.category import Category, SubCategory
from app.models.campus_products import CampusProduct
from flask_login import current_user
from app.utils import *
from sqlalchemy import or_

products = Blueprint("products", __name__, url_prefix="/store")

@products.route("/")
@require_clearance(1)
def show_products():
    category_id = request.args.get("category", type=int)
    subcategory_id = request.args.get("subcategory", type=int)
    brand = request.args.get("brand")
    search = request.args.get("search", type=str)
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
    if search:
        # Search by product name, category name, subcategory name, or brand
        campus_products_query = campus_products_query.join(
            SubCategory, Product.sub_category_id == SubCategory.id
        ).join(
            Category, SubCategory.category_id == Category.id
        ).filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Category.name.ilike(f"%{search}%"),
                SubCategory.name.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%")
            )
        )

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
                        <img src="{{ url_for('admin.serve_azure_image', filename=cp.product.image_gallery[0]) }}" class="card-img-top product-img" alt="{{ cp.product.name }}">   
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
            search=search,
        )

@products.route("/search_suggestions")
@require_clearance(1)
def search_suggestions():
    term = request.args.get("q", type=str)
    results = []
    if term:
        # Product name matches
        products = Product.query.filter(Product.name.ilike(f"%{term}%")).limit(5).all()
        results += [
            {"id": p.id, "name": p.name, "type": "product", "image": p.image_gallery[0] if p.image_gallery else ""}
            for p in products
        ]
        # Category matches
        categories = Category.query.filter(Category.name.ilike(f"%{term}%")).limit(3).all()
        results += [
            {"id": c.id, "name": c.name, "type": "category", "image": ""}
            for c in categories
        ]
        # SubCategory matches
        subcategories = SubCategory.query.filter(SubCategory.name.ilike(f"%{term}%")).limit(3).all()
        results += [
            {"id": sc.id, "name": sc.name, "type": "subcategory", "image": ""}
            for sc in subcategories
        ]
        # Brand matches
        brands = Product.query.with_entities(Product.brand).filter(Product.brand.ilike(f"%{term}%")).distinct().limit(3).all()
        results += [
            {"id": None, "name": b[0], "type": "brand", "image": ""}
            for b in brands if b[0]
        ]
    return jsonify(results)
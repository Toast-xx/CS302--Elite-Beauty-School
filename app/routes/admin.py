from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from app.utils import require_clearance
from app.utils import *
from app.models.user import User  
from app.models.campus import Campus
from app.models.order import Order
from app.models.product import Product
from app.models.campus_products import CampusProduct
from app.models.category import Category
from app.models.category import SubCategory
from collections import Counter
from datetime import datetime, timedelta
from app import db
from sqlalchemy.exc import IntegrityError

API_URL = "https://cs302-elite-beauty-school.onrender.com"

# Blueprint for admin-related routes
admin = Blueprint("admin", __name__)

def get_admin_campus():
    user_id = session.get('user_id')
    admin_user = User.query.get(user_id)
    if not admin_user:
        return None, None, None
    return admin_user.campus_id, admin_user.clearance_level, admin_user

@admin.route("/admin")
@require_clearance(2)
def admin_base():
    clearance = session.get('clearance_level')
    banner = "Dashboard"
    campus= session.get('campus')
    campuses = Campus.query.all()
    if clearance != 2:
        return redirect("/")
    return render_template("admin_base.html", clearance=clearance, banner=banner, campus=campus, campuses=campuses, api_url=API_URL)

@admin.route("/superadmin_dashboard")
@require_clearance(3)
def superadmin_dashboard():
    clearance = session.get('clearance_level')
    banner = "Dashboard"
    if clearance != 3:
        return redirect("/")
    campuses = Campus.query.all()
    return render_template("admin_base.html", clearance=clearance, banner=banner, campus="Super Admin", campuses=campuses, api_url=API_URL)

@admin.route("/dashboard_request", methods=["POST"])
def dashboard_request():
    try:
        data = request.json
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        campus = data.get("campus")

        # Convert dates
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Base query
        query = db.session.query(Order).join(User).join(Campus)
        query = query.filter(Order.created_at >= start_date, Order.created_at <= end_date)

        # Optional campus filter
        if campus not in ["All", "Super Admin"] and campus:
            query = query.filter(Campus.name == campus)

        orders = query.all()

        # ================= BASIC METRICS =======================
        completed_orders = [o for o in orders if o.status == "Completed"]
        orders_completed = len(completed_orders)
        total_sales = sum(float(o.total) for o in completed_orders)
        average_order_value = total_sales / orders_completed if orders_completed else 0

        # ================= TOP PRODUCTS =======================
        # Flatten all product names from completed orders
        all_items = []
        for order in completed_orders:
            for item in order.items:
                all_items.append(item.product.name)

        # Count products manually
        product_counts = Counter(all_items)
        top3 = product_counts.most_common(3)

        # Format pie chart data
        colors_pie = ['#f28e2b', '#e15759', '#59a14f']
        dataSetsPie = [
            {"value": count, "name": name, "itemStyle": {"color": colors_pie[idx] if idx < len(colors_pie) else "#000"}}
            for idx, (name, count) in enumerate(top3)
        ]
        top_product = top3[0][0] if top3 else "N/A"

        # ================= LAST 5 WEEKS =======================
        week_ranges = []
        for i in range(5, 0, -1):
            week_end = end_date - timedelta(days=(i - 1) * 7)
            week_start = week_end - timedelta(days=6)
            week_ranges.append((week_start, week_end))

        status_list = ["Completed", "Pending", "Cancelled", "Refunded"]
        diagram_data = {status: [0]*5 for status in status_list}

        for idx, (wk_start, wk_end) in enumerate(week_ranges):
            for order in orders:
                order_date = order.created_at.date()
                if wk_start.date() <= order_date <= wk_end.date() and order.status in status_list:
                    diagram_data[order.status][idx] += 1


        week_labels = [f"{w[0].strftime('%b %d')} - {w[1].strftime('%b %d')}" for w in week_ranges]
        colors_bar = {
            "Completed": "#59a14f",
            "Pending": "#f28e2b",
            "Cancelled": "#e15759",
            "Refunded": "#4e79a7"
        }

        dataSetsBar = [
            {"name": status, "data": diagram_data[status], "color": colors_bar[status]}
            for status in status_list
        ]

        response = {
            "dashboard": {
                "total_sales": round(total_sales, 2),
                "orders_completed": orders_completed,
                "average_order_value": round(average_order_value, 2),
                "top_product": top_product
            },
            "dataSetsPie": dataSetsPie,
            "dataSetsBar": dataSetsBar,
            "week_labels": week_labels
        }

        return jsonify(response)

    except Exception as ex:
        print("ERROR /dashboard_request:", ex)
        return jsonify({"error": "Internal server error"}), 500

@admin.route("/orders_request", methods=["POST"])
def orders_request():
    try:
        data = request.json
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        campus = data.get("campus")

        # Convert strings to datetime
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        # Base query
        query = (
            db.session.query(Order)
            .join(User, Order.user_id == User.id)
            .join(Campus, User.campus_id == Campus.id)
            .filter(Order.created_at >= start_date)
            .filter(Order.created_at <= end_date)
        )

        # Filter by campus if provided and not "All" or "Super Admin"
        if campus and campus not in ["All", "Super Admin"]:
            query = query.filter(Campus.name == campus)

        orders = query.all()

        # Format orders for JSON response
        order_list = [
            {
                "id": o.id,
                "user_id": o.user_id,
                "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status": o.status,
                "total": float(o.total)
            }
            for o in orders
        ]

        return jsonify({"orders": order_list})

    except Exception as ex:
        print("ERROR /orders_request:", ex)
        return jsonify({"error": "Internal server error"}), 500

@admin.route("/products_request", methods=["POST"])
def products_request():
    data = request.json
    campus = data.get("campus")
    query = db.session.query(CampusProduct).join(Product).join(SubCategory).join(Category).join(Campus)
    
    if campus and campus not in ["Super Admin", "All"]:
        query = query.filter(Campus.name == campus)
        
    campus_products = query.filter(CampusProduct.is_active == True).all()
    
    print("All CampusProducts:", campus_products)
    product_list = [
        {
            "id": cp.id,
            "name": cp.product.name,
            "brand": cp.product.brand,
            "description": cp.product.description,
            "category": cp.product.sub_category.category.name,
            "sub_category": cp.product.sub_category.name,
            "image": cp.product.image_gallery[0] if cp.product.image_gallery else None,
            "price": float(cp.price),
            "campus_quantity": cp.campus_quantity,
            "spa_quantity": cp.spa_quantity,
            "campus": cp.campus.name,
        }
        for cp in campus_products
    ]
    return jsonify({"products": product_list})

@admin.route("/inventory_request", methods=["POST"])
def inventory_request():
    data = request.json
    campus = data.get("campus")

    query = db.session.query(CampusProduct).join(Product).join(Campus)

    if campus and campus not in ["Super Admin", "All"]:
        query = query.filter(Campus.name == campus)

    campus_products = query.filter(CampusProduct.is_active == True).all()

    inventory_list = [
        {
            "id": cp.id,
            "name": cp.product.name,
            "campus_quantity": cp.campus_quantity,
            "spa_quantity":cp.spa_quantity,
        }
        for cp in campus_products
    ]
    
    lowstock_list = [
        {
            "id": cp.id,
            "name": cp.product.name,
            "campus_quantity": cp.campus_quantity,
        }
        for cp in campus_products if cp.campus_quantity < 5
    ]

    return jsonify({
        "inventory": inventory_list,
        "lowstock": lowstock_list
    })

@admin.route("/search_users", methods=['GET'])
def search_user():
    query = request.args.get("q", "").strip()
    campus_name = request.args.get("campus", "").strip()

    if not query:
        return jsonify([])

    filters = []
    # Filter by name or email
    filters.append(
        (User.name.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%"))
    )

    # Filter by campus if provided
    if campus_name and campus_name not in ["Super Admin", "All"]:
        filters.append(User.campus.has(Campus.name == campus_name))

    users = User.query.filter(*filters).all()

    user_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "campus_id": user.campus_id,
            "campus_name": user.campus.name if user.campus else None,
            "clearance_level": user.clearance_level,
            "start_date": str(user.start_date) if user.start_date else "",
            "end_date": str(user.end_date) if user.end_date else "",
            "active": user.active
        }
        for user in users
    ]
    return jsonify(user_list)

@admin.route("/admin/add_user", methods=["POST"])
@require_clearance(2)
def add_user():
    campus_id, clearance, admin_user = get_admin_campus()

    user_id = request.form.get("user_id")  # will exist if editing
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    campus_id_form = request.form.get("campus_id")
    clearance_level = int(request.form.get("clearance_level", 1))
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not all([name, email, campus_id_form]):
        return jsonify({"status": "error", "message": "All fields are required"}), 400

    # Only super admins can add super admin users
    if clearance_level == 3 and clearance != 3:
        return jsonify({"status": "error", "message": "Only super admins can add super admin users."}), 403

    try:
        if user_id:  # EDIT EXISTING USER
            user = User.query.get(user_id)
            if not user:
                return jsonify({"status": "error", "message": "User not found"}), 404

            existing_user = User.query.filter_by(email=email).first()
            if user.email != email and existing_user:
                return jsonify({"status": "error", "message": "Email already exists"}), 400

            user.name = name
            user.email = email
            user.campus_id = campus_id_form
            user.clearance_level = clearance_level
            user.start_date = start_date
            user.end_date = end_date
            if password:
                user.password_hash = hash_password(password)

        else:  # CREATE NEW USER
            if User.query.filter_by(email=email).first():
                return jsonify({"status": "error", "message": "Email already exists"}), 400

            user = User(
                name=name,
                email=email,
                password_hash=hash_password(password),
                campus_id=campus_id_form,
                clearance_level=clearance_level,
                start_date=start_date,
                end_date=end_date
            )
            db.session.add(user)

        db.session.commit()
        return jsonify({"status": "success", "user_id": user.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@admin.route("/search_products", methods=["GET"])
def search_products():
    query = request.args.get("q", "").strip()
    campus_name = request.args.get("campus", "").strip()

    if not query:
        return jsonify([])

    try:
        campus_products = (
            CampusProduct.query
            .join(Product, CampusProduct.product_id == Product.id)
            .join(Campus, CampusProduct.campus_id == Campus.id)
            .join(SubCategory, Product.sub_category_id == SubCategory.id)
            .join(Category, SubCategory.category_id == Category.id)
            .filter(Product.name.ilike(f"%{query}%"))
        )
        if campus_name and campus_name not in ["All", "Super Admin"]:
            campus_products = campus_products.filter(Campus.name == campus_name)

        campus_products = campus_products.filter(CampusProduct.is_active == True).all()

        product_list = [
            {
                "id": cp.id,
                "name": cp.product.name,
                "brand": cp.product.brand,
                "description": cp.product.description,
                "category": cp.product.sub_category.category.name,
                "sub_category": cp.product.sub_category.name,
                "image": cp.product.image_gallery[0] if cp.product.image_gallery else None,
                "price": float(cp.price),
                "campus_quantity": cp.campus_quantity,
                "spa_quantity": cp.spa_quantity,
                "campus": cp.campus.name,
            }
            for cp in campus_products
        ]
        return jsonify(product_list)

    except Exception as ex:
        print(f"Error in /search_products: {ex}")
        return jsonify({"error": "Internal server error"}), 500

@admin.route("/users_request", methods=["POST"])
def users_request():
    data = request.json
    campus_name = data.get("campus", "").strip()

    try:
        query = User.query.join(Campus, isouter=True)
        if campus_name and campus_name not in ["All", "Super Admin"]:
            query = query.filter(Campus.name == campus_name)

        users = query.all()

        user_list = [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "campus_id": u.campus_id,
                "campus_name": u.campus.name if u.campus else None,
                "clearance_level": u.clearance_level,
                "start_date": str(u.start_date) if u.start_date else None,
                "end_date": str(u.end_date) if u.end_date else None,
                "active": u.active
            }
            for u in users
        ]
        return jsonify({"users": user_list})

    except Exception as ex:
        print(f"Error in /users_request: {ex}")
        return jsonify({"error": "Internal server error"}), 500

@admin.route("/delete_product", methods=["POST"])
def delete_product():
    data = request.json
    cp_id = data.get("id")

    campus_product = CampusProduct.query.get(cp_id)
    if not campus_product:
        return jsonify({"success": False, "message": "Product not found"})

    campus_product.is_active = False
    db.session.commit()
    return jsonify({"success": True})

@admin.route("/update_product", methods=["POST"])
def update_product():
    data = request.get_json()

    if not data or "id" not in data:
        return jsonify({"success": False, "message": "Missing campus product ID"}), 400

    campus_product_id = data.pop("id")
    campus_product = CampusProduct.query.get(campus_product_id)

    if not campus_product:
        return jsonify({"success": False, "message": "Campus product not found"}), 404

    product = campus_product.product
    updated_fields = {}

    try:
        # --- Update Product name ---
        if "name" in data:
            name = str(data["name"]).strip()
            if name and name != product.name:
                product.name = name
                updated_fields["name"] = name

        # --- Update Product description ---
        if "description" in data:
            description = str(data["description"]).strip()
            if description != product.description:
                product.description = description
                updated_fields["description"] = description

        # --- Update CampusProduct price ---
        if "price" in data:
            raw_price = data["price"]
            try:
                new_price = float(raw_price)
            except (ValueError, TypeError):
                return jsonify({"success": False, "message": "Invalid price value"}), 400

            if new_price != float(campus_product.price):
                campus_product.price = new_price
                updated_fields["price"] = new_price

        # --- Update Product category ---
        if "category" in data:
            category_name = data["category"]
            if isinstance(category_name, dict):
                category_name = str(category_name.get("name", "")).strip()
            else:
                category_name = str(category_name).strip()

            if category_name:
                # Get or create Category
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                    db.session.flush()  # Assign ID

                # Keep existing sub-category name
                sub_category_name = product.sub_category.name if product.sub_category else "Default"
                sub_category = SubCategory.query.filter_by(
                    name=sub_category_name, category_id=category.id
                ).first()
                if not sub_category:
                    sub_category = SubCategory(name=sub_category_name, category_id=category.id)
                    db.session.add(sub_category)
                    db.session.flush()

                product.sub_category = sub_category
                updated_fields["category"] = category_name

        # --- Commit changes ---
        if not updated_fields:
            return jsonify({"success": False, "message": "No changes detected!"})

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Product updated successfully!",
            "updated_fields": updated_fields
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@admin.route('/update_quantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    campus_product_id = data.get("id")
    qty_to_add = data.get("quantity")
    qty_to_add = int(qty_to_add)
    print("Received ID:", campus_product_id)
    print("Received Quantity:", qty_to_add)
    if not campus_product_id or qty_to_add is None:
        return jsonify({"success": False, "message": "Missing id or quantity"}), 400

    product = CampusProduct.query.get(campus_product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    product.campus_quantity += qty_to_add
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Quantity updated",
        "new_quantity": product.campus_quantity
    })

@admin.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        # Convert dates from string to date objects
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None
        
        new_user = User(
            name=data['name'],
            email=data['email'],
            campus_id=int(data['campus_id']) if data.get('campus_id') else None,
            clearance_level=int(data['clearance_level']),
            active=bool(data['active']),
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success", "message": "User created successfully", "user_id": new_user.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================
# NEW ROUTE FOR ADD PRODUCT
# =========================
@admin.route("/add_product", methods=["POST"])
def add_product():
    import os
    import json
    from werkzeug.utils import secure_filename

    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    price = request.form.get('price', '').strip()
    brand = request.form.get('brand', '').strip()
    category_name = request.form.get('category', '').strip()
    images = request.files.getlist('images')
    category_id = request.form.get('category_id', '').strip()
    sub_category_id = request.form.get('sub_category_id', '').strip()

    # Get clearance level from session
    clearance = session.get('clearance_level')

# Validate
    if not name or not description or not price or not category_id or not sub_category_id:
       return jsonify({"success": False, "message": "Missing required fields"}), 400

    category = Category.query.get(category_id)
    sub_category = SubCategory.query.get(sub_category_id)
    if not category or not sub_category:
        return jsonify({"success": False, "message": "Invalid category or sub-category"}), 400


    try:
        price = float(price)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid price"}), 400

    # Find or create category and subcategory
    category = Category.query.get(category_id)
    sub_category = SubCategory.query.get(sub_category_id)
    if not category or not sub_category:
        return jsonify({"success": False, "message": "Invalid category or sub-category"}), 400


    # Save images to disk and collect filenames
    images = request.files.getlist('images')
    image_filenames = []
    for image in images:
        if image and image.filename:
            filename = secure_filename(image.filename)
            save_path = os.path.join('app', 'static', 'images', filename)
            image.save(save_path)
            image_filenames.append(filename)

    # Save product (sku removed)
    product = Product(
        name=name,
        brand=brand,
        description=description,
        sub_category_id=sub_category.id,
        image_gallery=image_filenames,  # Store filenames as JSON array
    )
    db.session.add(product)
    db.session.flush()

    if clearance == 3:  # Superadmin: multi-campus
        campus_ids = request.form.getlist('campus_ids')
        if not campus_ids:
            return jsonify({"success": False, "message": "Select at least one campus."}), 400
        for campus_id in campus_ids:
            campus = Campus.query.get(campus_id)
            if not campus:
                continue
            campus_product = CampusProduct(
                campus_id=campus.id,
                product_id=product.id,
                price=price,
                campus_quantity=0,
                spa_quantity=0
            )
            db.session.add(campus_product)

    # Get campus from session
    else:
     campus_name = session.get('campus')
    campus = Campus.query.filter_by(name=campus_name).first()
    if not campus:
        campus = Campus(name=campus_name)
        db.session.add(campus)
        db.session.flush()

    campus_product = CampusProduct(
        campus_id=campus.id,
        product_id=product.id,
        price=price,
        campus_quantity=0,
        spa_quantity=0
    )
    db.session.add(campus_product)
    db.session.commit()

    return jsonify({"success": True, "message": "Product added!", "images_saved": len(image_filenames)})

@admin.route("/get_categories_subcategories", methods=["GET"])
def get_categories_subcategories():
    categories = Category.query.all()
    sub_categories = SubCategory.query.all()
    return jsonify({
        "categories": [
            {"id": c.id, "name": c.name} for c in categories
        ],
        "sub_categories": [
            {"id": sc.id, "name": sc.name, "category_id": sc.category_id} for sc in sub_categories
        ]
    })
admin_bp = Blueprint('admin', __name__)

# --- CATEGORY ROUTES ---

@admin_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])

@admin_bp.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name required'}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 400
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name}), 201

# --- SUBCATEGORY ROUTES ---

@admin_bp.route('/subcategories', methods=['GET'])
def get_subcategories():
    subcategories = SubCategory.query.all()
    return jsonify([
        {'id': sc.id, 'name': sc.name, 'category_id': sc.category_id}
        for sc in subcategories
    ])

@admin_bp.route('/subcategories', methods=['POST'])
def add_subcategory():
    data = request.get_json()
    name = data.get('name')
    category_id = data.get('category_id')
    if not name or not category_id:
        return jsonify({'error': 'Name and category_id required'}), 400
    if SubCategory.query.filter_by(name=name, category_id=category_id).first():
        return jsonify({'error': 'SubCategory already exists'}), 400
    subcategory = SubCategory(name=name, category_id=category_id)
    db.session.add(subcategory)
    db.session.commit()
    return jsonify({'id': subcategory.id, 'name': subcategory.name, 'category_id': subcategory.category_id}), 201

# --- BRAND LOGIC (as string) ---

@admin_bp.route('/brands', methods=['GET'])
def get_brands():
    brands = db.session.query(Product.brand).distinct().filter(Product.brand.isnot(None)).all()
    brand_list = [b[0] for b in brands if b[0]]
    return jsonify(brand_list)

@admin_bp.route('/brands', methods=['POST'])
def add_brand():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name required'}), 400
    # No brand table, so just return success; actual brand is added when a product is created
    return jsonify({'name': name}), 201

# --- PRODUCT ROUTE ---

@admin_bp.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data.get('name')
    brand = data.get('brand')
    sub_category_id = data.get('sub_category_id')
    description = data.get('description')
    image_gallery = data.get('image_gallery')

    if not all([name, brand, sub_category_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    product = Product(
        name=name,
        brand=brand,
        sub_category_id=sub_category_id,
        description=description,
        image_gallery=image_gallery
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name}), 201
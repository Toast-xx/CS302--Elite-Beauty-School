from flask import Blueprint, jsonify, request, render_template
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
from datetime import timedelta
from datetime import datetime
from app import db


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
    campus_id, clearance, admin_user = get_admin_campus()
    if not campus_id:
        return redirect("/")
    # Super admin sees all users/campuses/roles, admin sees only their campus and roles
    if clearance == 3:
        users = User.query.all()
        campuses = Campus.query.all()
        allowed_roles = [1, 2, 3]
    else:
        users = User.query.filter_by(campus_id=campus_id).all()
        campuses = [Campus.query.get(campus_id)]
        allowed_roles = [1, 2]
    return render_template(
        "admin_base.html",
        items=users,
        campuses=campuses,
        allowed_roles=allowed_roles,
    )

@admin.route("/superadmin_dashboard")
@require_clearance(3)
def superadmin_dashboard():
    clearance = session.get('clearance_level')
    banner = "Dashboard"
    if clearance != 3:
        return redirect("/")
    return render_template("admin_base.html", clearance=clearance, banner=banner, campus="Super Admin")

@admin.route("/dashboard_request", methods=["POST"])
def dashboard_request():
    data = request.json
    start_date = datetime.datetime.strptime(data.get("start_date"), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(data.get("end_date"), "%Y-%m-%d")
    campus_id, clearance, _ = get_admin_campus()

    query = (
        db.session.query(Order)
        .join(User, Order.user_id == User.id)
        .join(Campus, User.campus_id == Campus.id)
        .filter(Order.created_at >= start_date)
        .filter(Order.created_at <= end_date)
    )
    if clearance != 3 and campus_id:
        query = query.filter(Campus.id == campus_id)

    orders = query.all()

    # Basic metrics
    orders_completed = sum(1 for o in orders if o.status == "Completed")
    total_sales = sum(float(o.total) for o in orders if o.status == "Completed")
    refunds = sum(1 for o in orders if o.status in ["Refunded", "Returned"])
    average_order_value = total_sales / orders_completed if orders_completed > 0 else 0

    # Top products
    all_items = [item.product.name for o in orders if o.status == "Completed" for item in o.items]
    product_counter = Counter(all_items)
    top3 = product_counter.most_common(3)
    colors_pie = ['#f28e2b', '#e15759', '#59a14f']
    dataSetsPie = [
        {"value": count, "name": name, "itemStyle": {"color": colors_pie[idx] if idx < len(colors_pie) else "#000"}}
        for idx, (name, count) in enumerate(top3)
    ]
    top_product = top3[0][0] if top3 else "N/A"

    # Weekly diagram
    week_ranges = []
    for i in range(5, 0, -1):
        week_end = end_date - timedelta(days=(i-1)*7)
        week_start = week_end - timedelta(days=6)
        week_ranges.append((week_start, week_end))

    status_list = ["Completed", "Pending", "Cancelled", "Refunded"]
    diagram_data = {status: [0]*5 for status in status_list}

    for idx, (start, end) in enumerate(week_ranges):
        for order in orders:
            if start <= order.created_at <= end and order.status in status_list:
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
            "refunds": refunds,
            "average_order_value": round(average_order_value, 2),
            "top_product": top_product
        },
        "dataSetsPie": dataSetsPie,
        "dataSetsBar": dataSetsBar,
        "week_labels": week_labels
    }
    return jsonify(response)

@admin.route("/orders_request", methods=["POST"])
def orders_request():
    data = request.json
    start_date = datetime.datetime.strptime(data.get("start_date"), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(data.get("end_date"), "%Y-%m-%d")
    campus_id, clearance, _ = get_admin_campus()

    query = (
        db.session.query(Order)
        .join(User, Order.user_id == User.id)
        .join(Campus, User.campus_id == Campus.id)
        .filter(Order.created_at >= start_date)
        .filter(Order.created_at <= end_date)
    )
    if clearance != 3 and campus_id:
        query = query.filter(Campus.id == campus_id)
    orders = query.all()
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

@admin.route("/products_request", methods=["POST"])
def products_request():
    data = request.json
    campus = data.get("campus")

    query = db.session.query(CampusProduct).join(Product).join(SubCategory).join(Category).join(Campus)

    if campus and campus not in ["Super Admin", "All"]:
        query = query.filter(Campus.name == campus)
        
    campus_products = query.all()
    
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

    campus_products = query.all()

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
    campus_id, clearance, _ = get_admin_campus()
    if not query:
        return jsonify([])

    filters = []
    if query:
        filters.append(
            (User.name.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        )
    if clearance != 3 and campus_id:
        filters.append(User.campus_id == campus_id)

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

@admin.route("/admin/add_user", methods=["GET", "POST"])
@require_clearance(2)
def add_user():
    campus_id, clearance, admin_user = get_admin_campus()
    # For GET: render form with correct campuses and roles
    if request.method == "GET":
        if clearance == 3:
            campuses = Campus.query.all()
            allowed_roles = [1, 2, 3]
        else:
            campuses = [Campus.query.get(campus_id)]
            allowed_roles = [1, 2]
        return render_template(
            "add_user.html",
            campuses=campuses,
            allowed_roles=allowed_roles
        )

    # For POST: process form submission
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    campus_id_form = request.form.get("campus_id")
    clearance_level = int(request.form.get("clearance_level", 1))
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    # Validate required fields
    if not all([name, email, campus_id_form]):
        error = "All fields are required"
        campuses = [Campus.query.get(campus_id)] if clearance != 3 else Campus.query.all()
        allowed_roles = [1, 2] if clearance != 3 else [1, 2, 3]
        return render_template("add_user.html", error=error, campuses=campuses, allowed_roles=allowed_roles), 400

    # Only super admins can add super admin users
    if clearance_level == 3 and clearance != 3:
        error = "Only super admins can add super admin users."
        campuses = [Campus.query.get(campus_id)] if clearance != 3 else Campus.query.all()
        allowed_roles = [1, 2] if clearance != 3 else [1, 2, 3]
        return render_template("add_user.html", error=error, campuses=campuses, allowed_roles=allowed_roles), 403

    if user_id:
        user = User.query.get(user_id)
        if not user:
            error = "User not found"
            campuses = [Campus.query.get(campus_id)] if clearance != 3 else Campus.query.all()
            allowed_roles = [1, 2] if clearance != 3 else [1, 2, 3]
            return render_template("add_user.html", error=error, campuses=campuses, allowed_roles=allowed_roles), 404
        existing_user = User.query.filter_by(email=email).first()
        if user.email != email and existing_user and existing_user.id != user.id:
            error = "User with this email already exists"
            campuses = [Campus.query.get(campus_id)] if clearance != 3 else Campus.query.all()
            allowed_roles = [1, 2] if clearance != 3 else [1, 2, 3]
            return render_template("add_user.html", error=error, campuses=campuses, allowed_roles=allowed_roles), 400
        user.name = name
        user.email = email
        user.campus_id = campus_id_form
        user.clearance_level = clearance_level
        user.start_date = start_date
        user.end_date = end_date
        if password:
            user.password_hash = hash_password(password)
    else:
        if User.query.filter_by(email=email).first():
            error = "User with this email already exists"
            campuses = [Campus.query.get(campus_id)] if clearance != 3 else Campus.query.all()
            allowed_roles = [1, 2] if clearance != 3 else [1, 2, 3]
            return render_template("add_user.html", error=error, campuses=campuses, allowed_roles=allowed_roles), 400
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
    try:
        db.session.commit()
        return redirect(url_for('admin.admin_base', success=1))
    except Exception as ex:
        print(f"Error in /search_users: {ex}")
        return jsonify({"error": "Internal server error"}), 500

@admin.route("/search_products", methods=["GET"])
def search_products():
    query = request.args.get("q", "").strip()
    campus_id, clearance, campus_name = get_admin_campus()

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

        # apply campus filter if not Super Admin
        if campus_name not in ["All", "Super Admin"]:
            campus_products = campus_products.filter(Campus.id == campus_id)

        campus_products = campus_products.all()

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


@admin.route("/delete_product", methods=["POST"])
def delete_product():
    data = request.json
    cp_id = data.get("id")

    campus_product = CampusProduct.query.get(cp_id)
    if not campus_product:
        return jsonify({"success": False, "message": "Product not found"})

    db.session.delete(campus_product)
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

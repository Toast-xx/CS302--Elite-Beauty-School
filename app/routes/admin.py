import datetime
from flask import Blueprint, jsonify, request, render_template
from app.utils import require_clearance
from app.utils import *
from app.models.user import User 
from app.models.campus import Campus
from app.models.order import Order
from app.models.product import Product
from app.models.campus_products import CampusProduct
from collections import Counter
from datetime import timedelta


admin = Blueprint("admin", __name__)

@admin.route("/admin")
@require_clearance(2)  # Only users with clearance_level >= 2 can access
def admin_base1():
    clearance = session.get('clearance_level')
    banner="Dashboard"
    campus=session.get('campus')
    if session.get('clearance_level') != 2:
        return redirect("/")
    return render_template("admin_base.html", clearance=clearance,banner=banner,campus=campus)

@admin.route("/superadmin_dashboard")
@require_clearance(3)  # Only users with clearance_level >= 3 can access
def admin_base():
    clearance = session.get('clearance_level')
    banner="Dashboard"
    if session.get('clearance_level') != 3:
        return redirect("/")
    return render_template("admin_base.html", clearance=clearance, banner=banner,campus="Super Admin")

@admin.route("/dashboard_request", methods=["POST"])
def dashboard_request():
    data = request.json
    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d")
    campus = data.get("campus")

    query = (
        db.session.query(Order)
        .join(User, Order.user_id == User.id)
        .join(Campus, User.campus_id == Campus.id)
        .filter(Order.created_at >= start_date)
        .filter(Order.created_at <= end_date)
    )
    if campus and campus not in ["Super Admin", "All"]:
        query = query.filter(Campus.name == campus)

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
    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d")
    campus = data.get("campus")

    query = (
        db.session.query(Order)
        .join(User, Order.user_id == User.id)
        .join(Campus, User.campus_id == Campus.id)
        .filter(Order.created_at >= start_date)
        .filter(Order.created_at <= end_date)
    )
    if campus and campus not in ["Super Admin", "All"]:
        query = query.filter(Campus.name == campus)
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

    query = db.session.query(CampusProduct).join(Product).join(Campus)

    if campus and campus not in ["Super Admin", "All"]:
        query = query.filter(Campus.name == campus)
    campus_products = query.all()
    product_list = [
        {
            "id": cp.id,
            "name": cp.product.name,
            "brand": cp.product.brand,
            "description": cp.product.description,
            "image": cp.product.image_gallery[0] if cp.product.image_gallery else None,
            "price": float(cp.price),
            "campus_quantity": cp.campus_quantity,
            "spa_quantity": cp.spa_quantity,
            "campus": cp.campus.name,
        }
        for cp in campus_products
    ]

    return jsonify({"products": product_list})

@admin.route("/search_users", methods=['GET'])
def search_user():
    query = request.args.get("q", "").strip()
    campus = request.args.get("campus", "All")

    if not query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        users_query = User.query.filter(User.clearance_level == 1)
        users_query = users_query.filter(User.name.ilike(f"%{query}%"))

        if campus and campus not in ["All", "Super Admin"]:
            users_query = users_query.join(Campus, User.campus_id == Campus.id)
            users_query = users_query.filter(Campus.name == campus)

        users = users_query.all()

        user_list = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "campus_id": user.campus_id,
                "campus_name": user.campus.name if hasattr(user, 'campus') else None
            }
            for user in users
        ]

        return jsonify(user_list)

    except Exception as ex:
        print(f"Error in /search_users: {ex}")
        return jsonify({"error": "Internal server error"}), 500


@admin.route("/search_products", methods=['GET'])
def search_products():
    query = request.args.get("q", "").strip()
    campus = request.args.get("campus", "All")

    if not query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        campus_products = (
            CampusProduct.query
            .join(Product, CampusProduct.product_id == Product.id)
            .join(Campus, CampusProduct.campus_id == Campus.id)
            .filter(Product.name.ilike(f"%{query}%")) 
        )
        if campus and campus not in ["All", "Super Admin"]:
            campus_products = campus_products.filter(Campus.name == campus)

        campus_products = campus_products.all()

        product_list = [
            {
                "id": cp.id,
                "name": cp.product.name,
                "brand": cp.product.brand,
                "description": cp.product.description,
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

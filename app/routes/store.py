from flask import Blueprint, render_template
from app.models.product import Product

products = Blueprint("products", __name__, url_prefix="/store")

@products.route("/")
def show_products():
    # Fetch all products from the database
    #product_list = Product.query.all()
    # Placeholder face and skin care products
    product_list = [
        {"name": "Daily Microfoliant", "brand": "Dermalogica", "price": 89.99, "image_file": "placeholder1.jpg"},
        {"name": "Active C Serum", "brand": "Aspect Dr", "price": 119.99, "image_file": "placeholder1.jpg"},
        {"name": "Hydrating Oil Capsules", "brand": "Environ", "price": 99.99, "image_file": "placeholder1.jpg"},
        {"name": "Hydro-Dynamic Ultimate Moisture", "brand": "Murad", "price": 129.99, "image_file": "placeholder1.jpg"},
        {"name": "3-in-1 Fruit Peel Mask", "brand": "O Cosmedics", "price": 79.99, "image_file": "placeholder1.jpg"},
        {"name": "Ultra B2 Hydrating Serum", "brand": "Ultraceuticals", "price": 109.99, "image_file": "placeholder1.jpg"},
        {"name": "Hydra3Ha Intensive Cream", "brand": "Sothys", "price": 149.99, "image_file": "placeholder1.jpg"},
        {"name": "Hydrating Collagen Mask", "brand": "Thalgo", "price": 69.99, "image_file": "placeholder1.jpg"},
    ]
    return render_template("store.html", products=product_list)

"""
Model for linking products to campuses and tracking campus-specific inventory.
Each CampusProduct entry associates a product with a campus and stores the available quantity.
"""

from app.models.product import Product
from app import db

class CampusProduct(db.Model):
    """
    Represents a product's inventory and price for a specific campus.
    Tracks both campus (online) and spa (training) quantities.
    """
    __tablename__ = "campus_products"

    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    campus_quantity = db.Column(db.Integer, default=0)  # For online purchases
    spa_quantity = db.Column(db.Integer, default=0)     # For internal SPA/training use

    product = db.relationship("Product", backref="campus_products")
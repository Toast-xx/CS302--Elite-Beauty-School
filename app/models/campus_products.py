# Model for linking products to campuses and tracking campus-specific inventory.
# Each CampusProduct entry associates a product with a campus and stores the available quantity.
# Ensure foreign key references match the related Campus and Product models.
from app.models.product import Product
from app import db

class CampusProduct(db.Model):
    __tablename__ = "campus_products"

    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    campus_quantity = db.Column(db.Integer, default=0)

    product = db.relationship("Product", backref="campus_products")
    
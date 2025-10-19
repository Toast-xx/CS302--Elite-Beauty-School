# Model for linking products to campuses and tracking campus-specific inventory.
# Each CampusProduct entry associates a product with a campus and stores the available quantity.
# Ensure foreign key references match the related Campus and Product models.

from app import db

class CampusProduct(db.Model):
    __tablename__ = "campus_products"

    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    campus_quantity = db.Column(db.Integer, default=0)  
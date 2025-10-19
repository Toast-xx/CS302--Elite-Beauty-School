# Product model for the products table.
# Represents store products with fields for name, price, brand, category, description, images, campus, and quantity.
# Includes a helper to_dict() for serialization. Ensure foreign keys match related models.

from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'), nullable=False)
    description = db.Column(db.Text, nullable=True) 
    image_gallery = db.Column(db.JSON, nullable=True)      # e.g., ['img1.jpg', 'img2.jpg']
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)  

    def __repr__(self):
        return f"<Product {self.name}>"

    def to_dict(self):
        # Converts product instance to dictionary for API or template use
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
            "description": self.description,
            "category": self.category,  # Note: 'category' property must exist or be defined elsewhere
            "image_gallery": self.image_gallery,
            "campus_id": self.campus_id,
        }
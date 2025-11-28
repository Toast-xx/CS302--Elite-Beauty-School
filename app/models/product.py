# Product model for the products table.
# Represents store products with fields for name, price, brand, category, description, images, campus, and quantity.
# Includes a helper to_dict() for serialization. Ensure foreign keys match related models.

from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=True)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_gallery = db.Column(db.JSON, nullable=True)
   


    def __repr__(self):
        return f"<Product {self.name}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "description": self.description,
            "category": self.category,
            "image_gallery": self.image_gallery,
            
        }
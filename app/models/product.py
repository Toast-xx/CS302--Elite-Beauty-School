from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(100), nullable=True) 
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    image_gallery = db.Column(db.JSON, nullable=True)      # e.g., ['img1.jpg', 'img2.jpg']
    campus_id = db.Column(db.Integer, db.ForeignKey('campuses.id'), nullable=False)
    

    def __repr__(self):
        return f"<Product {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "brand": self.brand,
            "description": self.description,
            "category": self.category,
            "image_gallery": self.image_gallery,
            "campus_id": self.campus_id,
        }

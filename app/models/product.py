from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(100), nullable=True) 
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    image_file = db.Column(db.String(255), nullable=True)  # e.g., 'product1.jpg'
    image_gallery = db.Column(db.JSON, nullable=True)      # e.g., ['img1.jpg', 'img2.jpg']
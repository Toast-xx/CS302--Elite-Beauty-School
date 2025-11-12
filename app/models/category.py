"""
 Models for product categories and subcategories.
 Category has a one-to-many relationship with SubCategory.
 SubCategory has a one-to-many relationship with Product.
 Ensure foreign key and relationship names match those in related models.
"""
from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)

class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    products = db.relationship('Product', backref='sub_category', lazy=True)
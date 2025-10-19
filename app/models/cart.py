# Models for shopping cart and cart items.
# Cart is linked to a user and contains multiple CartItems.
# CartItem links to a product and tracks quantity.
# Cascade delete ensures cart items are removed when a cart is deleted.
# The product relationship in CartItem allows easy access to product details.

from app import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    # Relationship to Product for convenient access to product details
    product = db.relationship('Product')